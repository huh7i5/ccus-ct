# 🌱 CCUS知识图谱项目运行指南

## 项目概述

本项目是一个专门针对CCUS（碳捕集利用与封存）领域的知识图谱系统，包含完整的数据处理、知识抽取和Web服务功能。

## 📊 项目特点

- **781条记录** - 完整的CCUS领域文本数据
- **37,148个关系三元组** - 丰富的实体关系网络
- **10个实体类型** - 技术、项目、机构、地理、政策等
- **RESTful API** - 标准化的Web接口
- **中文支持** - 专业CCUS术语处理

## 🚀 快速启动

### 方法1：一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/huh7i5/ccus-ct.git
cd ccus-ct

# 一键启动
./start.sh
```

### 方法2：完整安装

```bash
# 1. 安装依赖
pip install flask flask-cors py2neo opencc-python-reimplemented thefuzz jieba

# 2. 构建知识图谱（首次运行）
python main.py --project ccus_project

# 3. 启动Web服务
cd server && python main.py
```

### 方法3：Python启动器

```bash
# 使用完整功能的Python启动器
python run_ccus_project.py
```

## 🔗 API接口

启动成功后，以下接口可用：

### 基础接口
- **GET** `http://localhost:8000/` - 服务状态检查
- **GET** `http://localhost:8000/graph/` - 获取知识图谱数据
- **POST** `http://localhost:8000/chat/` - CCUS问答接口

### 使用示例

```bash
# 检查服务状态
curl http://localhost:8000/

# 获取知识图谱数据
curl http://localhost:8000/graph/

# CCUS问答测试
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是CCUS技术？", "history": []}'
```

## 📁 项目结构

```
ccus-ct/
├── data/                          # 数据文件
│   ├── raw_data_ccus.txt         # 原始CCUS数据
│   ├── cleaned_ccus_data.txt     # 清洗后数据
│   ├── ccus_schema.json          # CCUS schema定义
│   └── ccus_project/             # 知识图谱数据
│       ├── base.json             # 基础三元组
│       ├── base_filtered.json    # 过滤后数据
│       └── base_refined.json     # 精炼后数据
├── modules/                       # 核心模块
│   ├── knowledge_graph_builder.py
│   ├── model_trainer.py
│   └── prepare/                  # 数据预处理
├── server/                       # Web服务
│   ├── app/                      # Flask应用
│   └── main.py                   # 服务器入口
├── start.sh                     # 快速启动脚本
├── run_ccus_project.py          # Python启动器
└── main.py                      # 知识图谱构建入口
```

## 🛠️ 技术栈

- **后端框架**: Flask + Flask-CORS
- **知识抽取**: 基于规则的实体关系抽取
- **数据处理**: jieba分词 + 自定义CCUS schema
- **API标准**: RESTful API
- **数据格式**: JSON

## 📋 系统要求

- Python 3.7+
- 8GB+ RAM（用于知识图谱构建）
- 5GB+ 磁盘空间

## 🔧 故障排除

### 常见问题

1. **端口8000被占用**
   ```bash
   # 查找占用进程
   lsof -i :8000
   # 终止进程
   kill -9 <PID>
   ```

2. **依赖包安装失败**
   ```bash
   # 使用清华源
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package_name>
   ```

3. **知识图谱构建失败**
   ```bash
   # 删除旧数据重新构建
   rm -rf data/ccus_project/
   python main.py --project ccus_project
   ```

4. **内存不足**
   ```bash
   # 减少批处理大小
   # 编辑modules/prepare/process.py中的batch_size参数
   ```

## 📈 性能优化

- **数据缓存**: 知识图谱数据自动缓存，避免重复构建
- **分批处理**: 大量数据分批处理，减少内存占用
- **异步加载**: Web服务支持异步请求处理

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

## 📞 联系方式

- **项目地址**: https://github.com/huh7i5/ccus-ct.git
- **问题反馈**: GitHub Issues
- **邮箱**: 1322133227@qq.com

## 🎯 未来计划

- [ ] 集成大语言模型增强问答能力
- [ ] 添加图数据库（Neo4j）支持
- [ ] 实现实时数据更新
- [ ] 开发可视化界面
- [ ] 支持多语言（英文）

---

**开始使用CCUS知识图谱系统，探索碳捕集利用与封存技术的知识世界！** 🌍