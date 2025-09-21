#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCUS知识图谱项目简化启动器 - 绕过PyTorch兼容性问题
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def check_knowledge_graph():
    """检查知识图谱数据是否存在"""
    kg_path = Path("data/ccus_project/base.json")
    if kg_path.exists():
        # 统计记录数
        with open(kg_path, 'r', encoding='utf-8') as f:
            records = sum(1 for line in f if line.strip())

        # 统计关系数
        total_relations = 0
        with open(kg_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    total_relations += len(data.get('relationMentions', []))

        print(f"  ✅ 知识图谱数据已存在")
        print(f"     - 记录数: {records}")
        print(f"     - 关系数: {total_relations}")
        return True
    else:
        print(f"  ❌ 知识图谱数据不存在: {kg_path}")
        return False

def start_server():
    """启动服务器"""
    print("\n🚀 启动Web服务器...")

    # 检查端口是否被占用
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()

        if result == 0:
            print("  ✅ 服务器已在运行 (端口8000)")
            return True
    except:
        pass

    # 启动新的服务器
    server_dir = Path("server")
    if not server_dir.exists():
        print("  ❌ server目录不存在")
        return False

    os.chdir(server_dir)

    try:
        # 后台启动服务器
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待启动
        time.sleep(3)

        # 检查是否成功启动
        if process.poll() is None:
            print("  ✅ 服务器启动成功")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"  ❌ 服务器启动失败: {stderr.decode()}")
            return False

    except Exception as e:
        print(f"  ❌ 启动服务器时出错: {e}")
        return False

def test_apis():
    """测试API接口"""
    print("\n🧪 测试API接口...")

    try:
        import requests

        # 测试主页
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("  ✅ 主页接口: 正常")
            else:
                print(f"  ❌ 主页接口: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 主页接口: {e}")

        # 测试知识图谱接口
        try:
            response = requests.get("http://localhost:8000/graph/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                record_count = len(data.get('data', []))
                print(f"  ✅ 知识图谱接口: 正常 ({record_count} 条记录)")
            else:
                print(f"  ❌ 知识图谱接口: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 知识图谱接口: {e}")

        # 测试聊天接口
        try:
            chat_data = {"prompt": "什么是CCUS技术？", "history": []}
            response = requests.post("http://localhost:8000/chat/",
                                   json=chat_data, timeout=5)
            if response.status_code == 200:
                print("  ✅ 聊天接口: 正常")
            else:
                print(f"  ❌ 聊天接口: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 聊天接口: {e}")

    except ImportError:
        print("  ⚠️  requests模块未安装，跳过API测试")
        print("     安装命令: pip install requests")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 CCUS知识图谱项目简化启动器")
    print("=" * 60)

    print("\n📁 检查项目文件...")

    # 检查知识图谱数据
    if not check_knowledge_graph():
        print("\n⚠️  知识图谱数据不存在，请先运行以下命令构建:")
        print("   python main.py --project ccus_project")
        print("\n或者使用简化脚本:")
        print("   ./start.sh")
        return

    # 启动服务器
    if not start_server():
        print("\n❌ 服务器启动失败")
        return

    # 测试API
    test_apis()

    print("\n" + "=" * 60)
    print("🎉 CCUS知识图谱项目启动成功！")
    print("=" * 60)
    print("📊 服务信息:")
    print("  🌐 API服务: http://localhost:8000")
    print("  📖 API文档:")
    print("    GET  /          - 服务状态")
    print("    GET  /graph/    - 知识图谱数据")
    print("    POST /chat/     - CCUS问答")
    print("\n🧪 快速测试:")
    print("  curl http://localhost:8000/")
    print("  curl http://localhost:8000/graph/")
    print("\n📋 使用说明:")
    print("  • 服务器在后台运行")
    print("  • 如需停止: pkill -f 'python main.py'")
    print("  • 重新启动: python start_simple.py")
    print("\n🔗 项目地址: https://github.com/huh7i5/ccus-ct.git")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        print("请检查项目文件完整性或使用其他启动方式")