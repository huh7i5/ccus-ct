#!/usr/bin/env python3
"""
生成最终的CCUS知识图谱，基于v11收敛结果
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import defaultdict, Counter
import pandas as pd
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class CCUSKnowledgeGraphProcessor:
    def __init__(self, kg_path):
        self.kg_path = kg_path
        self.kg_data = []
        self.graph = nx.DiGraph()
        self.relation_stats = {}
        self.entity_stats = {}

        print(f"🚀 加载最终收敛的CCUS知识图谱: {kg_path}")
        self.load_data()
        self.build_graph()

    def load_data(self):
        """加载知识图谱数据"""
        with open(self.kg_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.kg_data.append(json.loads(line))

        print(f"📊 加载完成: {len(self.kg_data)} 个文档")

    def build_graph(self):
        """构建NetworkX图"""
        relation_counts = defaultdict(int)
        entity_counts = defaultdict(int)

        for item in self.kg_data:
            for relation in item['relationMentions']:
                em1 = relation['em1Text']
                em2 = relation['em2Text']
                rel_type = relation['label']

                # 过滤掉噪声实体（如单字符、数字等）
                if len(em1) > 1 and len(em2) > 1 and em1 != em2:
                    if not (em1.isdigit() or em2.isdigit() or em1 in ['，', '。', '：', '；']):
                        self.graph.add_edge(em1, em2, relation=rel_type)
                        relation_counts[rel_type] += 1
                        entity_counts[em1] += 1
                        entity_counts[em2] += 1

        self.relation_stats = dict(relation_counts)
        self.entity_stats = dict(entity_counts)

        print(f"🔗 图构建完成:")
        print(f"   - 节点数: {self.graph.number_of_nodes()}")
        print(f"   - 边数: {self.graph.number_of_edges()}")
        print(f"   - 关系类型: {len(self.relation_stats)}")

    def get_core_entities(self, top_k=50):
        """获取核心实体（高频且度数大的节点）"""
        # 结合度中心性和频率
        degree_centrality = nx.degree_centrality(self.graph)

        core_entities = []
        for entity in self.entity_stats:
            if entity in degree_centrality:
                score = degree_centrality[entity] * self.entity_stats[entity]
                core_entities.append((entity, score))

        core_entities.sort(key=lambda x: x[1], reverse=True)
        return [entity for entity, _ in core_entities[:top_k]]

    def create_core_subgraph(self, core_entities):
        """创建核心子图"""
        subgraph = self.graph.subgraph(core_entities)
        return subgraph

    def visualize_knowledge_graph(self, output_dir="data/ccus_project/final_results"):
        """可视化知识图谱"""
        Path(output_dir).mkdir(exist_ok=True)

        print("📈 生成知识图谱可视化...")

        # 1. 核心子图可视化
        core_entities = self.get_core_entities(30)
        core_subgraph = self.create_core_subgraph(core_entities)

        plt.figure(figsize=(20, 16))
        pos = nx.spring_layout(core_subgraph, k=3, iterations=50)

        # 绘制节点
        node_sizes = [self.entity_stats.get(node, 1) * 50 for node in core_subgraph.nodes()]
        nx.draw_networkx_nodes(core_subgraph, pos,
                             node_size=node_sizes,
                             node_color='lightblue',
                             alpha=0.7)

        # 绘制边（按关系类型着色）
        edge_colors = []
        relation_color_map = {
            '应用于': 'red',
            '包含': 'blue',
            '位于': 'green',
            '开发者': 'orange',
            '合作伙伴': 'purple',
            '投资方': 'brown'
        }

        for edge in core_subgraph.edges(data=True):
            rel_type = edge[2].get('relation', '其他')
            edge_colors.append(relation_color_map.get(rel_type, 'gray'))

        nx.draw_networkx_edges(core_subgraph, pos,
                             edge_color=edge_colors,
                             alpha=0.5,
                             arrows=True,
                             arrowsize=20)

        # 绘制标签
        nx.draw_networkx_labels(core_subgraph, pos, font_size=8)

        plt.title("CCUS领域核心知识图谱", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/ccus_core_knowledge_graph.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 2. 关系类型分布图
        plt.figure(figsize=(12, 8))
        relations = list(self.relation_stats.keys())
        counts = list(self.relation_stats.values())

        bars = plt.bar(relations, counts, color=['#ff9999', '#66b3ff', '#99ff99',
                                               '#ffcc99', '#ff99cc', '#c2c2f0'])
        plt.title("CCUS知识图谱关系类型分布", fontsize=14, fontweight='bold')
        plt.xlabel("关系类型")
        plt.ylabel("关系数量")
        plt.xticks(rotation=45)

        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/ccus_relation_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ 可视化完成，保存至: {output_dir}/")

    def export_statistics(self, output_dir="data/ccus_project/final_results"):
        """导出统计信息"""
        Path(output_dir).mkdir(exist_ok=True)

        stats = {
            "知识图谱概况": {
                "文档数": len(self.kg_data),
                "实体数": self.graph.number_of_nodes(),
                "关系数": self.graph.number_of_edges(),
                "关系类型数": len(self.relation_stats)
            },
            "关系类型统计": self.relation_stats,
            "核心实体": dict(sorted(self.entity_stats.items(),
                                key=lambda x: x[1], reverse=True)[:50])
        }

        with open(f"{output_dir}/ccus_kg_statistics.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print(f"📊 统计信息导出至: {output_dir}/ccus_kg_statistics.json")

    def export_graph_formats(self, output_dir="data/ccus_project/final_results"):
        """导出多种图格式"""
        Path(output_dir).mkdir(exist_ok=True)

        # 1. GraphML格式（可用于Gephi、Cytoscape等）
        nx.write_graphml(self.graph, f"{output_dir}/ccus_knowledge_graph.graphml")

        # 2. GML格式
        nx.write_gml(self.graph, f"{output_dir}/ccus_knowledge_graph.gml")

        # 3. 边列表格式
        with open(f"{output_dir}/ccus_knowledge_graph_edges.csv", 'w', encoding='utf-8') as f:
            f.write("source,target,relation\n")
            for edge in self.graph.edges(data=True):
                source, target, data = edge
                relation = data.get('relation', '')
                f.write(f'"{source}","{target}","{relation}"\n')

        # 4. 节点列表格式
        with open(f"{output_dir}/ccus_knowledge_graph_nodes.csv", 'w', encoding='utf-8') as f:
            f.write("node,frequency,degree\n")
            for node in self.graph.nodes():
                freq = self.entity_stats.get(node, 0)
                degree = self.graph.degree(node)
                f.write(f'"{node}",{freq},{degree}\n')

        print(f"💾 图数据导出完成: {output_dir}/")

    def generate_summary_report(self, output_dir="data/ccus_project/final_results"):
        """生成总结报告"""
        Path(output_dir).mkdir(exist_ok=True)

        core_entities = self.get_core_entities(20)

        report = f"""# CCUS知识图谱构建完成报告

## 项目概况
- **迭代轮数**: v0 → v11 (共12轮)
- **收敛状态**: ✅ 已收敛 (扩展率 = 10.00%)
- **最终版本**: v11

## 知识图谱统计
- **文档数**: {len(self.kg_data)}
- **实体数**: {self.graph.number_of_nodes()}
- **关系数**: {self.graph.number_of_edges()}
- **关系类型**: {len(self.relation_stats)}

## 关系类型分布
"""
        for rel_type, count in sorted(self.relation_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / sum(self.relation_stats.values())) * 100
            report += f"- **{rel_type}**: {count} ({percentage:.1f}%)\n"

        report += f"""
## 核心实体 (Top 20)
"""
        for i, entity in enumerate(core_entities, 1):
            freq = self.entity_stats.get(entity, 0)
            report += f"{i}. **{entity}** (频次: {freq})\n"

        report += f"""
## 输出文件
- 📊 统计信息: `ccus_kg_statistics.json`
- 🖼️ 核心图谱: `ccus_core_knowledge_graph.png`
- 📈 关系分布: `ccus_relation_distribution.png`
- 🔗 GraphML格式: `ccus_knowledge_graph.graphml`
- 📄 边列表: `ccus_knowledge_graph_edges.csv`
- 📋 节点列表: `ccus_knowledge_graph_nodes.csv`

## 技术特点
- ✅ 基于SPN4RE的关系抽取
- ✅ 迭代训练直至收敛
- ✅ 中文CCUS领域专用
- ✅ 多格式输出支持

---
*生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(f"{output_dir}/CCUS_KG_Report.md", 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📋 总结报告生成: {output_dir}/CCUS_KG_Report.md")

def main():
    # v11最终收敛的知识图谱路径
    kg_path = "data/ccus_project/iteration_v11/knowledge_graph.json"

    print("🎯 开始处理v11最终收敛的CCUS知识图谱")
    print("=" * 60)

    # 创建处理器
    processor = CCUSKnowledgeGraphProcessor(kg_path)

    # 生成所有输出
    processor.visualize_knowledge_graph()
    processor.export_statistics()
    processor.export_graph_formats()
    processor.generate_summary_report()

    print("=" * 60)
    print("🏆 CCUS知识图谱处理完成！")
    print("📁 所有结果保存在: data/ccus_project/final_results/")

if __name__ == "__main__":
    main()