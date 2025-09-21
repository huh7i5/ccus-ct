# CCUS-CT 数据目录

本目录存储CCUS知识图谱构建过程中的所有数据文件。

## 目录结构说明

```
data/
├── clean_data.txt                      # 清洗后的原始文本数据
├── clean_data_res_*.json              # 处理结果文件
├── project_v1/                        # 项目版本1数据
│   ├── base.json                      # 基础知识图谱
│   ├── base_filtered.json             # 过滤后的基础图谱
│   ├── base_refined.json              # 精炼的基础图谱
│   ├── iter_v0.json                   # 迭代版本0
│   ├── history/                       # 历史版本记录
│   └── iteration_v0/                  # 迭代数据
│       ├── alphabet.json              # 实体字典
│       ├── knowledge_graph.json       # 知识图谱数据
│       ├── prediction.json            # 预测结果
│       └── running_log.txt           # 运行日志
└── __init__.py                        # Python包初始化文件
```

## 数据说明

- **原始数据**: CCUS技术领域的专业文献和技术资料
- **处理数据**: 经过清洗、标注和结构化处理的数据
- **知识图谱**: 构建的CCUS领域知识图谱文件
- **迭代数据**: 图谱构建过程中的迭代优化数据

## 使用说明

1. 原始数据放置在根目录下
2. 处理后的数据按项目版本组织
3. 每个迭代版本包含完整的训练和测试数据

## 作者
- huh7i5 <1322133227@qq.com>
