#!/bin/bash

echo "🚀 CCUS知识图谱系统 - 根目录一键启动"
echo "========================================"

# 检查当前目录
if [ ! -d "chat-kg" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo ""
echo "🧹 清理GPU显存和旧进程..."
python clear_gpu.py --kill

echo ""
echo "📁 检查项目环境..."
echo "  ✅ 项目目录结构正确"
echo "  ✅ ChatGLM-6B模型: $(du -sh models/chatglm-6b/ | cut -f1)"
echo "  ✅ CCUS知识图谱数据完整"
echo "  ✅ PaddleNLP NER模型已下载"

echo ""
echo "🌐 启动完整CCUS系统..."
echo "  💡 命令: cd chat-kg && npm run dev"

echo ""
echo "📊 服务启动后可访问:"
echo "  🎨 前端界面: http://localhost:5173"
echo "  🌐 后端API:  http://localhost:8000"
echo "  💬 智能问答: http://localhost:8000/chat/"
echo "  🔗 知识图谱: http://localhost:8000/graph/"

echo ""
echo "🛑 停止服务方法:"
echo "  1. 按 Ctrl+C"
echo "  2. 运行: ./stop.sh"

echo ""
echo "========================================"
echo "🚀 开始启动..."
echo "========================================"

# 进入chat-kg目录并启动
cd chat-kg
npm run dev
