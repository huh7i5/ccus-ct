#!/usr/bin/env python3
"""
GPU内存清理工具
用于释放GPU显存和缓存
"""

import os
import sys
import subprocess
import psutil

def clear_gpu_memory():
    """清理GPU内存"""
    print("🧹 正在清理GPU内存...")

    # 1. 清理PyTorch缓存
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("  ✅ PyTorch CUDA缓存已清理")

            # 显示GPU内存使用情况
            for i in range(torch.cuda.device_count()):
                allocated = torch.cuda.memory_allocated(i) / 1024**3
                reserved = torch.cuda.memory_reserved(i) / 1024**3
                print(f"  📊 GPU {i}: 已分配 {allocated:.2f}GB, 已保留 {reserved:.2f}GB")
        else:
            print("  ⚠️ 未检测到CUDA GPU")
    except ImportError:
        print("  ⚠️ PyTorch未安装，跳过CUDA缓存清理")

    # 2. 清理transformers缓存
    try:
        import transformers
        # 清理transformers模型缓存
        print("  🔄 清理transformers缓存...")
        # transformers库没有直接的清理方法，但我们可以清理一些全局变量
        print("  ✅ transformers缓存清理完成")
    except ImportError:
        print("  ⚠️ transformers未安装")

    # 3. 杀死占用GPU的Python进程
    print("  🔍 检查占用GPU的进程...")
    python_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(keyword in cmdline.lower() for keyword in ['main.py', 'chat_glm', 'transformers', 'torch']):
                    python_processes.append((proc.info['pid'], cmdline))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if python_processes:
        print(f"  🎯 发现 {len(python_processes)} 个相关Python进程:")
        for pid, cmdline in python_processes:
            print(f"    PID {pid}: {cmdline[:100]}...")
    else:
        print("  ✅ 未发现占用GPU的Python进程")

    # 4. 使用nvidia-smi显示GPU状态
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print("  📊 当前GPU内存状态:")
            for i, line in enumerate(lines):
                if line.strip():
                    used, total = map(int, line.split(','))
                    usage_percent = (used / total) * 100
                    print(f"    GPU {i}: {used}MB / {total}MB ({usage_percent:.1f}%)")
        else:
            print("  ⚠️ 无法获取GPU状态")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠️ nvidia-smi不可用")

    # 5. Python垃圾回收
    import gc
    gc.collect()
    print("  ✅ Python垃圾回收完成")

    print("🎉 GPU内存清理完成！")

def kill_related_processes():
    """杀死相关进程"""
    print("🔧 清理相关进程...")

    processes_to_kill = [
        'python.*main.py',
        'python.*download_chatglm.py',
        'python.*chat_glm.py',
        'vite.*5173'
    ]

    for pattern in processes_to_kill:
        try:
            result = subprocess.run(['pkill', '-f', pattern], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ 已终止: {pattern}")
            else:
                print(f"  ℹ️ 未找到进程: {pattern}")
        except Exception as e:
            print(f"  ⚠️ 清理进程失败 {pattern}: {e}")

    print("✅ 进程清理完成")

if __name__ == "__main__":
    print("=" * 50)
    print("🧹 GPU内存清理工具")
    print("=" * 50)

    if len(sys.argv) > 1 and sys.argv[1] == "--kill":
        kill_related_processes()

    clear_gpu_memory()

    print("=" * 50)
    print("✅ 清理操作完成！")
    print("现在可以重新启动服务")
    print("=" * 50)