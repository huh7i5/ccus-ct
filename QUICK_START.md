# 🚀 CCUS知识图谱项目 - 快速启动指南

## 📊 项目状态

- ✅ **已构建完成**: 781条记录，37,148个关系三元组
- ✅ **服务运行中**: http://localhost:8000
- ✅ **所有API正常**: 状态、知识图谱、问答接口

## 🎯 三种启动方式

### 1. 简化启动器（推荐 - 无依赖冲突）

```bash
python start_simple.py
```

**特点**:
- ✅ 绕过PyTorch版本冲突
- ✅ 自动检测服务状态
- ✅ 完整API测试
- ✅ 无需额外依赖

### 2. Shell脚本启动

```bash
chmod +x start.sh
./start.sh
```

**特点**:
- ✅ 一键启动
- ✅ 自动端口检测
- ✅ 后台运行

### 3. 手动启动

```bash
# 进入服务器目录
cd server

# 启动Flask服务
python main.py
```

## 🔗 API接口使用

### 基础测试

```bash
# 检查服务状态
curl http://localhost:8000/

# 获取知识图谱数据（781条记录）
curl http://localhost:8000/graph/

# CCUS问答测试
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是CCUS技术？", "history": []}'
```

### Python API调用示例

```python
import requests
import json

# 获取知识图谱数据
response = requests.get('http://localhost:8000/graph/')
kg_data = response.json()
print(f"知识图谱记录数: {len(kg_data['data'])}")

# CCUS问答
chat_data = {
    "prompt": "深部咸水层封存的优势是什么？",
    "history": []
}
response = requests.post('http://localhost:8000/chat/', json=chat_data)
result = response.json()
print(f"回答: {result['response']}")
```

## 🛠️ 故障排除

### 问题1: PyTorch版本冲突
```
错误: module 'torch.utils._pytree' has no attribute 'register_pytree_node'
```
**解决方案**: 使用简化启动器
```bash
python start_simple.py
```

### 问题2: 端口被占用
```bash
# 查找占用进程
lsof -i :8000
# 终止进程
pkill -f "python main.py"
```

### 问题3: 知识图谱数据丢失
```bash
# 重新构建知识图谱
python main.py --project ccus_project
```

## 📁 项目文件说明

```
项目根目录/
├── start_simple.py       # 简化启动器（推荐）
├── start.sh             # Shell启动脚本
├── run_ccus_project.py  # 完整启动器（有依赖冲突）
├── main.py              # 知识图谱构建
├── data/                # 数据文件
│   ├── ccus_project/    # 知识图谱数据
│   ├── cleaned_ccus_data.txt  # 清洗后文本
│   └── ccus_schema.json # CCUS schema
└── server/              # Web服务
    ├── main.py          # 服务器入口
    └── app/             # Flask应用
```

## 🎉 成功标志

看到以下输出说明启动成功：

```
🎉 CCUS知识图谱项目启动成功！
📊 服务信息:
  🌐 API服务: http://localhost:8000
  📖 API文档:
    GET  /          - 服务状态
    GET  /graph/    - 知识图谱数据
    POST /chat/     - CCUS问答
```

## 📊 项目特色

- **781条CCUS记录** - 完整的领域知识覆盖
- **37,148个关系三元组** - 丰富的实体关系网络
- **10个实体类型** - 技术、项目、机构、地理、政策等
- **中文专业术语** - 完整的CCUS中文术语支持
- **RESTful API** - 标准化接口，易于集成

## 🔄 重启/停止服务

```bash
# 停止服务
pkill -f "python main.py"

# 重新启动
python start_simple.py
```

## 📞 技术支持

- **项目地址**: https://github.com/huh7i5/ccus-ct.git
- **问题反馈**: GitHub Issues
- **邮箱**: 1322133227@qq.com

---

**现在就开始使用CCUS知识图谱系统吧！** 🌱