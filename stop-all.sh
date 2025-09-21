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
