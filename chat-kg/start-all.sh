#!/bin/bash

echo "🚀 CCUS知识图谱系统一键启动脚本"
echo "======================================"

# 清除显存
echo "🧹 正在清除GPU显存..."
if command -v nvidia-smi &> /dev/null; then
    # 杀死所有Python进程释放显存
    echo "  终止现有Python进程..."
    pkill -f "python.*main.py" 2>/dev/null || true
    pkill -f "python.*download_chatglm.py" 2>/dev/null || true

    # 等待一下让进程完全退出
    sleep 2

    # 显示当前显存使用情况
    echo "  当前GPU状态:"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "    GPU显存: " $1 "MB / " $2 "MB"}'

    # 清理GPU缓存
    echo "  清理GPU缓存..."
    python3 -c "
import torch
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print('    ✅ GPU缓存已清理')
else:
    print('    ⚠️ 未检测到CUDA GPU')
" 2>/dev/null || echo "    ⚠️ 无法清理GPU缓存"

else
    echo "  ⚠️ 未检测到nvidia-smi，跳过GPU清理"
fi

# 检查并创建必要目录
echo ""
echo "📁 检查项目目录..."
cd "$(dirname "$0")/.." || exit 1

if [ ! -d "models" ]; then
    echo "  创建models目录..."
    mkdir -p models
fi

if [ ! -d "data/ccus_project" ]; then
    echo "  ❌ 知识图谱数据不存在，请先运行: python main.py --project ccus_project"
    exit 1
fi

echo "  ✅ 项目目录检查完成"

# 检查依赖
echo ""
echo "🔍 检查系统依赖..."

# 检查Python依赖
python3 -c "
import sys
required_packages = ['flask', 'flask_cors', 'transformers', 'torch', 'jieba', 'opencc']
missing = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f'  ✅ {package}')
    except ImportError:
        missing.append(package)
        print(f'  ❌ {package}')

if missing:
    print(f'  缺少依赖: {missing}')
    print('  请运行: pip install ' + ' '.join(missing))
    sys.exit(1)
else:
    print('  ✅ Python依赖检查完成')
"

if [ $? -ne 0 ]; then
    exit 1
fi

# 检查Node.js依赖
cd chat-kg
if [ ! -d "node_modules" ]; then
    echo "  📦 安装前端依赖..."
    npm install
fi
cd ..

# 启动后端服务
echo ""
echo "🌐 启动后端服务..."
cd server
python3 main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "  等待后端服务启动..."
sleep 5

# 检查后端是否成功启动
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "  ✅ 后端服务启动成功 (PID: $BACKEND_PID)"
    echo "     API地址: http://localhost:8000"
else
    echo "  ❌ 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 启动前端服务
echo ""
echo "🎨 启动前端服务..."
cd chat-kg
npm run dev &
FRONTEND_PID=$!
cd ..

# 等待前端启动
echo "  等待前端服务启动..."
sleep 3

# 检查前端是否成功启动
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "  ✅ 前端服务启动成功 (PID: $FRONTEND_PID)"
    echo "     界面地址: http://localhost:5173"
else
    echo "  ⚠️ 前端服务可能需要更长时间启动"
    echo "     界面地址: http://localhost:5173 (请稍后访问)"
fi

# 显示启动完成信息
echo ""
echo "======================================"
echo "🎉 CCUS知识图谱系统启动完成！"
echo "======================================"
echo "📊 服务信息:"
echo "  🌐 后端API:  http://localhost:8000"
echo "  🎨 前端界面: http://localhost:5173"
echo "  💬 智能问答: http://localhost:8000/chat/"
echo "  🔗 知识图谱: http://localhost:8000/graph/"
echo ""
echo "📋 进程信息:"
echo "  后端进程: $BACKEND_PID"
echo "  前端进程: $FRONTEND_PID"
echo ""
echo "🛑 停止服务:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo "  或者按 Ctrl+C 然后运行停止脚本"
echo ""
echo "🔗 项目地址: https://github.com/huh7i5/ccus-ct.git"
echo "======================================"

# 创建停止脚本
cat > stop-all.sh << 'EOF'
#!/bin/bash
echo "🛑 停止CCUS知识图谱系统..."

# 停止Python后端服务
echo "  停止后端服务..."
pkill -f "python.*main.py" 2>/dev/null && echo "    ✅ 后端服务已停止" || echo "    ⚠️ 未找到运行的后端服务"

# 停止Node.js前端服务
echo "  停止前端服务..."
pkill -f "vite.*5173" 2>/dev/null && echo "    ✅ 前端服务已停止" || echo "    ⚠️ 未找到运行的前端服务"

# 清理GPU内存
echo "  清理GPU内存..."
python3 -c "
import torch
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print('    ✅ GPU缓存已清理')
" 2>/dev/null || echo "    ⚠️ 无法清理GPU缓存"

echo "✅ 系统已完全停止"
EOF

chmod +x stop-all.sh
echo "💾 已创建停止脚本: ./stop-all.sh"

# 保持脚本运行，等待用户中断
echo ""
echo "🎮 系统正在运行中..."
echo "   按 Ctrl+C 停止所有服务"

# 处理中断信号
trap 'echo -e "\n🛑 收到停止信号，正在关闭服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; ./stop-all.sh; exit 0' INT

# 监控服务状态
while true; do
    sleep 10

    # 检查后端状态
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "⚠️ 后端服务意外停止"
        break
    fi

    # 检查前端状态
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "⚠️ 前端服务意外停止"
        break
    fi
done

echo "❌ 服务异常退出"
./stop-all.sh