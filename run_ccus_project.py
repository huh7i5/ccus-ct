#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCUS知识图谱项目启动脚本
"""

import os
import sys
import subprocess
import time
import signal
import webbrowser
from pathlib import Path

class CCUSProjectManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.server_process = None

    def check_dependencies(self):
        """检查Python依赖"""
        print("🔍 检查项目依赖...")
        required_packages = [
            'flask', 'flask-cors', 'py2neo', 'opencc-python-reimplemented',
            'thefuzz', 'jieba', 'transformers', 'torch'
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package}")

        if missing_packages:
            print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
            print("正在安装...")
            for package in missing_packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package])

    def check_data_files(self):
        """检查数据文件"""
        print("\n📁 检查数据文件...")

        # 检查原始数据
        raw_data = self.project_root / "data" / "raw_data_ccus.txt"
        if not raw_data.exists():
            print("  ❌ 原始CCUS数据文件不存在")
            return False
        print(f"  ✅ 原始数据: {raw_data}")

        # 检查清洗后数据
        cleaned_data = self.project_root / "data" / "cleaned_ccus_data.txt"
        if not cleaned_data.exists():
            print("  ⚠️  清洗后数据不存在，需要运行数据清洗")
            return False
        print(f"  ✅ 清洗数据: {cleaned_data}")

        # 检查知识图谱数据
        kg_data = self.project_root / "data" / "ccus_project" / "base.json"
        if not kg_data.exists():
            print("  ⚠️  知识图谱数据不存在，需要重新构建")
            return False
        print(f"  ✅ 知识图谱: {kg_data}")

        return True

    def build_knowledge_graph(self):
        """构建知识图谱"""
        print("\n🔨 构建CCUS知识图谱...")

        os.chdir(self.project_root)
        cmd = [sys.executable, "main.py", "--project", "ccus_project"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            if result.returncode == 0:
                print("  ✅ 知识图谱构建成功")
                return True
            else:
                print(f"  ❌ 构建失败: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("  ⏰ 构建超时（30分钟）")
            return False

    def start_server(self):
        """启动Web服务器"""
        print("\n🚀 启动Web服务器...")

        server_dir = self.project_root / "server"
        os.chdir(server_dir)

        # 启动服务器进程
        self.server_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待服务器启动
        time.sleep(3)

        if self.server_process.poll() is None:
            print("  ✅ 服务器启动成功")
            print("  🌐 服务地址: http://localhost:8000")
            return True
        else:
            print("  ❌ 服务器启动失败")
            return False

    def test_apis(self):
        """测试API接口"""
        print("\n🧪 测试API接口...")

        import requests

        try:
            # 测试主页
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("  ✅ 主页接口正常")

            # 测试知识图谱接口
            response = requests.get("http://localhost:8000/graph/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ 知识图谱接口正常 ({len(data.get('data', []))} 条记录)")

            # 测试聊天接口
            chat_data = {"prompt": "什么是CCUS技术？", "history": []}
            response = requests.post("http://localhost:8000/chat/",
                                   json=chat_data, timeout=5)
            if response.status_code == 200:
                print("  ✅ 聊天接口正常")

            return True

        except requests.RequestException as e:
            print(f"  ❌ API测试失败: {e}")
            return False

    def create_demo_page(self):
        """创建演示页面"""
        demo_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCUS知识图谱演示</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .api-test { margin: 10px 0; }
        button { padding: 10px 15px; margin: 5px; cursor: pointer; }
        #result { background: #f5f5f5; padding: 15px; margin-top: 10px; white-space: pre-wrap; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { text-align: center; padding: 15px; background: #e8f4f8; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 CCUS知识图谱系统</h1>
            <p>碳捕集利用与封存技术知识图谱演示平台</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <h3>781</h3>
                <p>记录数量</p>
            </div>
            <div class="stat-box">
                <h3>37,148</h3>
                <p>关系三元组</p>
            </div>
            <div class="stat-box">
                <h3>10</h3>
                <p>实体类型</p>
            </div>
        </div>

        <div class="section">
            <h2>🔍 API接口测试</h2>
            <div class="api-test">
                <button onclick="testStatus()">测试服务状态</button>
                <button onclick="loadKnowledgeGraph()">加载知识图谱</button>
                <button onclick="testChat()">测试CCUS问答</button>
            </div>
            <div id="result"></div>
        </div>

        <div class="section">
            <h2>💬 CCUS问答系统</h2>
            <input type="text" id="question" placeholder="请输入CCUS相关问题..." style="width: 70%; padding: 10px;">
            <button onclick="askQuestion()" style="padding: 10px 20px;">提问</button>
            <div id="chatResult"></div>
        </div>
    </div>

    <script>
        function displayResult(data, elementId = 'result') {
            document.getElementById(elementId).textContent = JSON.stringify(data, null, 2);
        }

        async function testStatus() {
            try {
                const response = await fetch('/');
                const data = await response.json();
                displayResult(data);
            } catch (error) {
                displayResult({error: error.message});
            }
        }

        async function loadKnowledgeGraph() {
            try {
                const response = await fetch('/graph/');
                const data = await response.json();
                displayResult({
                    message: data.message,
                    recordCount: data.data.length,
                    sample: data.data.slice(0, 2)
                });
            } catch (error) {
                displayResult({error: error.message});
            }
        }

        async function testChat() {
            try {
                const response = await fetch('/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        prompt: '什么是CCUS技术？',
                        history: []
                    })
                });
                const data = await response.json();
                displayResult(data);
            } catch (error) {
                displayResult({error: error.message});
            }
        }

        async function askQuestion() {
            const question = document.getElementById('question').value;
            if (!question) return;

            try {
                const response = await fetch('/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        prompt: question,
                        history: []
                    })
                });
                const data = await response.json();
                displayResult(data, 'chatResult');
            } catch (error) {
                displayResult({error: error.message}, 'chatResult');
            }
        }
    </script>
</body>
</html>"""

        demo_path = self.project_root / "server" / "static" / "demo.html"
        demo_path.parent.mkdir(exist_ok=True)

        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write(demo_html)

        print(f"  ✅ 演示页面已创建: {demo_path}")
        return demo_path

    def cleanup(self, signum=None, frame=None):
        """清理资源"""
        print("\n🧹 正在关闭服务...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        print("  ✅ 服务已关闭")
        sys.exit(0)

    def run(self):
        """运行完整流程"""
        print("=" * 50)
        print("🚀 CCUS知识图谱项目启动器")
        print("=" * 50)

        # 注册信号处理
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        try:
            # 1. 检查依赖
            self.check_dependencies()

            # 2. 检查数据文件
            if not self.check_data_files():
                print("\n⚠️  数据文件不完整，正在重新构建...")
                if not self.build_knowledge_graph():
                    print("❌ 项目启动失败")
                    return

            # 3. 启动服务器
            if not self.start_server():
                print("❌ 项目启动失败")
                return

            # 4. 测试API
            time.sleep(2)
            self.test_apis()

            # 5. 创建演示页面
            demo_path = self.create_demo_page()

            print("\n" + "=" * 50)
            print("🎉 CCUS知识图谱项目启动成功！")
            print("=" * 50)
            print("📊 服务信息:")
            print("  🌐 API服务: http://localhost:8000")
            print("  📱 演示页面: http://localhost:8000/static/demo.html")
            print("  📖 API文档:")
            print("    GET  /          - 服务状态")
            print("    GET  /graph/    - 知识图谱数据")
            print("    POST /chat/     - CCUS问答")
            print("\n📋 使用说明:")
            print("  • 浏览器访问演示页面进行交互测试")
            print("  • 使用curl或其他工具调用API接口")
            print("  • 按 Ctrl+C 停止服务")
            print("\n🔗 项目地址: https://github.com/huh7i5/ccus-ct.git")
            print("=" * 50)

            # 等待用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

        except Exception as e:
            print(f"❌ 启动过程中发生错误: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    manager = CCUSProjectManager()
    manager.run()