# 🚀 CCUS知识图谱系统 - 一键启动指南

## 📋 一键启动功能

现在您可以使用 `npm run dev` 一键启动整个CCUS知识图谱系统！

### 🎯 功能特点

- 🧹 **自动清理GPU显存** - 启动前释放所有GPU内存
- 🌐 **同时启动前后端** - Flask后端 + Vue前端
- 🔍 **智能检查依赖** - 自动验证Python和Node.js依赖
- 📊 **实时状态监控** - 监控服务运行状态
- 🛑 **优雅停止服务** - Ctrl+C或npm run stop

## 🚀 快速使用

### 方法1：npm一键启动（推荐）

```bash
# 进入前端目录
cd chat-kg

# 一键启动前后端
npm run dev
```

### 方法2：直接运行脚本

```bash
# 进入前端目录
cd chat-kg

# 直接运行启动脚本
./start-all.sh
```

### 方法3：GPU清理后启动

```bash
# 先清理GPU内存
python clear_gpu.py --kill

# 然后启动系统
cd chat-kg && npm run dev
```

## 📊 启动过程

启动脚本会自动执行以下步骤：

1. **🧹 清理GPU显存**
   - 终止现有Python进程
   - 清理PyTorch CUDA缓存
   - 显示GPU内存状态

2. **📁 检查项目环境**
   - 验证必要目录存在
   - 检查知识图谱数据
   - 确认依赖安装完整

3. **🌐 启动后端服务**
   - 启动Flask API服务器
   - 加载ChatGLM-6B模型
   - 初始化CCUS知识图谱

4. **🎨 启动前端服务**
   - 启动Vue开发服务器
   - 热更新和实时编译

5. **📊 状态监控**
   - 实时检查服务状态
   - 自动故障恢复

## 🎮 可用命令

### 启动命令

```bash
npm run dev        # 一键启动前后端
npm run start      # 同 npm run dev
npm run stop       # 停止所有服务
```

### 单独启动

```bash
npm run dev-frontend-only    # 仅启动前端
npm run server              # 前端开发服务器（对外访问）
npm run build              # 构建生产版本
```

### 维护命令

```bash
python clear_gpu.py        # 清理GPU内存
python clear_gpu.py --kill # 清理GPU内存并终止进程
./stop-all.sh             # 停止所有服务（自动创建）
```

## 📊 服务信息

启动成功后，您可以访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| 🎨 前端界面 | http://localhost:5173 | Vue 3用户界面 |
| 🌐 后端API | http://localhost:8000 | Flask RESTful API |
| 💬 智能问答 | http://localhost:8000/chat/ | ChatGLM问答接口 |
| 🔗 知识图谱 | http://localhost:8000/graph/ | 知识图谱数据接口 |

## 🔧 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 清理端口
   python clear_gpu.py --kill
   ```

2. **GPU内存不足**
   ```bash
   # 清理GPU显存
   python clear_gpu.py
   ```

3. **依赖缺失**
   ```bash
   # 安装Python依赖
   pip install flask flask-cors transformers torch jieba opencc-python-reimplemented

   # 安装Node.js依赖
   cd chat-kg && npm install
   ```

4. **知识图谱数据缺失**
   ```bash
   # 重新构建知识图谱
   python main.py --project ccus_project
   ```

### 错误诊断

启动脚本会自动诊断以下问题：

- ✅ GPU显存使用情况
- ✅ Python依赖完整性
- ✅ Node.js依赖状态
- ✅ 项目目录结构
- ✅ 知识图谱数据
- ✅ 服务端口可用性

## 🎯 高级用法

### 自定义GPU清理

```python
# 创建自定义清理脚本
import torch
torch.cuda.empty_cache()  # 清理CUDA缓存
import gc; gc.collect()   # Python垃圾回收
```

### 修改启动配置

编辑 `chat-kg/start-all.sh` 文件可以：

- 修改GPU清理策略
- 调整依赖检查项目
- 自定义启动顺序
- 配置监控间隔

### 生产环境部署

```bash
# 构建前端
npm run build

# 使用production服务器
npm run preview

# 或使用nginx + gunicorn部署
```

## 📈 性能优化建议

1. **GPU内存管理**
   - 定期运行 `python clear_gpu.py`
   - 监控GPU使用率
   - 避免多个模型同时加载

2. **系统资源优化**
   - 确保有足够的内存（推荐16GB+）
   - 使用SSD提升IO性能
   - 关闭不必要的后台程序

3. **网络优化**
   - 使用局域网访问前端界面
   - 启用HTTP/2和压缩
   - 配置CDN加速静态资源

## 🎉 使用体验

一键启动后，您将拥有：

- 🌱 **专业CCUS界面** - 现代化的绿色主题
- 🤖 **ChatGLM-6B驱动** - 6B参数大模型智能问答
- 🔗 **知识图谱增强** - 37,148个专业关系三元组
- 💬 **流式对话体验** - 实时响应，自然交互
- 📊 **可视化展示** - 图谱关系和统计信息

---

**🚀 现在就试试 `npm run dev` 一键启动您的CCUS知识图谱系统吧！**