#!/bin/bash

echo "🛑 正在停止CCUS知识图谱系统..."
echo "================================="

# 杀死相关进程
python clear_gpu.py --kill

echo ""
echo "🧹 清理完成！"
echo "✅ 所有服务已停止"
echo "✅ GPU内存已清理"
