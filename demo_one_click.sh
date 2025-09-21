#!/bin/bash

echo "🎬 CCUS知识图谱系统一键启动演示"
echo "=================================="

echo ""
echo "📋 当前项目状态:"
echo "  ✅ CCUS知识图谱: 781条记录，37,148个关系三元组"
echo "  ✅ ChatGLM-6B: 模型框架已集成"
echo "  ✅ Vue 3前端: 现代化界面"
echo "  ✅ Flask后端: RESTful API"

echo ""
echo "🧹 GPU内存状态:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | awk '{print "  GPU: " $1 "MB / " $2 "MB (" int($1/$2*100) "%)"}'
else
    echo "  ⚠️ 未检测到nvidia-smi"
fi

echo ""
echo "🎯 现在演示一键启动功能:"
echo "  命令: cd chat-kg && npm run dev"

echo ""
echo "📊 启动流程包括:"
echo "  1. 🧹 自动清理GPU显存"
echo "  2. 📁 检查项目依赖和目录"
echo "  3. 🌐 启动Flask后端服务器"
echo "  4. 🎨 启动Vue前端开发服务器"
echo "  5. 📊 实时监控服务状态"

echo ""
echo "🔗 启动完成后可访问:"
echo "  前端界面: http://localhost:5173"
echo "  后端API:  http://localhost:8000"

echo ""
echo "🛑 停止服务方法:"
echo "  方法1: 按 Ctrl+C"
echo "  方法2: npm run stop"
echo "  方法3: ./stop-all.sh"

echo ""
echo "=================================="
echo "🚀 现在开始演示..."
echo "=================================="

# 等待用户确认
read -p "按Enter键开始演示，或Ctrl+C取消..."

echo ""
echo "🧹 首先清理GPU内存和现有服务..."
python clear_gpu.py --kill

echo ""
echo "⏳ 等待清理完成..."
sleep 2

echo ""
echo "🚀 现在使用一键启动: cd chat-kg && npm run dev"
echo ""

cd chat-kg
npm run dev