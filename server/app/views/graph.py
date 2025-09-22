import os
import json
from flask import request, Blueprint, jsonify
from thefuzz import process


mod = Blueprint('graph', __name__, url_prefix='/api')


def convert_relations_to_graph(relation_data):
    """将关系数据转换为ECharts图谱格式"""
    nodes = {}
    links = []
    link_dict = {}  # 用于去重和统计连线重要性

    for item in relation_data:
        relations = item.get('relationMentions', [])

        for relation in relations:
            em1 = relation.get('em1Text', '')
            em2 = relation.get('em2Text', '')
            label = relation.get('label', '')

            if em1 and em2:  # 显示所有实体，不过滤长度
                # 创建链接唯一标识符
                link_key = f"{em1}|{em2}"

                # 统计连线出现频次作为重要性指标
                if link_key not in link_dict:
                    link_dict[link_key] = {
                        'source': em1,
                        'target': em2,
                        'labels': [label],
                        'count': 1
                    }
                else:
                    link_dict[link_key]['count'] += 1
                    if label not in link_dict[link_key]['labels']:
                        link_dict[link_key]['labels'].append(label)

                # 添加节点
                if em1 not in nodes:
                    nodes[em1] = {
                        'name': em1,
                        'symbolSize': 30,
                        'category': 0
                    }

                if em2 not in nodes:
                    nodes[em2] = {
                        'name': em2,
                        'symbolSize': 30,
                        'category': 1
                    }

    # 按重要性排序并转换为边列表
    sorted_links = sorted(link_dict.values(), key=lambda x: x['count'], reverse=True)

    for link_info in sorted_links:
        # 合并多个关系标签
        label = link_info['labels'][0] if len(link_info['labels']) == 1 else f"{link_info['labels'][0]}等{len(link_info['labels'])}种关系"

        links.append({
            'source': link_info['source'],
            'target': link_info['target'],
            'value': label,
            'name': label,
            'weight': link_info['count'],  # 连线权重
            'lineStyle': {
                'color': '#bbb',
                'width': min(3, 1 + link_info['count'] * 0.2)  # 根据重要性调整线条粗细
            }
        })

    # 转换为列表格式
    node_list = list(nodes.values())

    # 由于数据质量已显著提升，可以显示所有连线
    # 如果连线数量过多才进行限制
    if len(links) > 2000:
        # 保留前2000条最重要的连线
        links = links[:2000]

    # 添加类别信息
    categories = [
        {'name': '实体1', 'itemStyle': {'color': '#5470c6'}},
        {'name': '实体2', 'itemStyle': {'color': '#91cc75'}}
    ]

    print(f"📊 图谱统计: {len(node_list)} 个节点, {len(links)} 条连线")

    return {
        'nodes': node_list,
        'links': links,
        'categories': categories
    }


@mod.route('/graph', methods=['GET'])
def graph():
    # Load CCUS knowledge graph data - using v11 final converged version
    ccus_data_path = '/root/KnowledgeGraph-based-on-Raw-text-A27-main/KnowledgeGraph-based-on-Raw-text-A27-main/data/ccus_project/iteration_v11/knowledge_graph.json'

    print(f"🔍 查找数据文件: {ccus_data_path}")
    print(f"📁 文件存在: {os.path.exists(ccus_data_path)}")

    if os.path.exists(ccus_data_path):
        try:
            with open(ccus_data_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                relation_data = [json.loads(line.strip()) for line in lines if line.strip()]

            # 转换为图谱格式，使用所有数据
            graph_data = convert_relations_to_graph(relation_data)

            return jsonify({
                'data': graph_data,
                'message': 'CCUS Knowledge Graph v11 (Final Converged Version) Loaded!'
            })
        except Exception as e:
            return jsonify({
                'data': {"error": f"Failed to load data: {str(e)}"},
                'message': 'Error loading graph data'
            }), 500
    else:
        return jsonify({
            'data': {"error": "CCUS knowledge graph data not found"},
            'message': 'Data file not found'
        }), 404


# @mod.route('/search', methods=['GET'])
# def get_triples():
#     # 获取参数
#     user_input = request.args.get('search')
#     result = search_node_item(user_input)

#     return jsonify({
#         'data': result,
#         'message': 'Got it!'
#     })
