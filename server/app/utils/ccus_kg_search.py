#!/usr/bin/env python3
"""
CCUS知识图谱搜索模块
实现基于实体的知识图谱检索和子图抽取
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import jieba

class CCUSKnowledgeGraphSearcher:
    def __init__(self):
        self.kg_data = []
        self.entity_index = defaultdict(list)  # 实体到记录的索引
        self.relation_index = defaultdict(list)  # 关系到记录的索引
        self.loaded = False
        self.load_knowledge_graph()

    def load_knowledge_graph(self):
        """加载CCUS知识图谱数据 - 完全修正最终版本"""
        kg_paths = [
            "../data/ccus_project/iteration_v11/knowledge_graph_ultimate_clean.json",
            "/root/KnowledgeGraph-based-on-Raw-text-A27-main/KnowledgeGraph-based-on-Raw-text-A27-main/data/ccus_project/iteration_v11/knowledge_graph_ultimate_clean.json",
            "../../data/ccus_project/iteration_v11/knowledge_graph_ultimate_clean.json"
        ]

        for kg_path in kg_paths:
            if os.path.exists(kg_path):
                try:
                    with open(kg_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f):
                            if line.strip():
                                data = json.loads(line)
                                self.kg_data.append(data)

                    print(f"✅ 加载知识图谱: {len(self.kg_data)} 条记录")
                    self._build_indexes()
                    self.loaded = True
                    return

                except Exception as e:
                    print(f"加载知识图谱失败: {e}")

        print("⚠️ 未找到CCUS知识图谱数据")

    def _build_indexes(self):
        """构建实体和关系索引"""
        print("构建知识图谱索引...")

        for idx, record in enumerate(self.kg_data):
            # 索引句子中的所有实体
            relations = record.get('relationMentions', [])

            entities = set()
            for rel in relations:
                em1 = rel.get('em1Text', '')
                em2 = rel.get('em2Text', '')
                label = rel.get('label', '')

                if em1:
                    entities.add(em1)
                    self.entity_index[em1].append(idx)

                if em2:
                    entities.add(em2)
                    self.entity_index[em2].append(idx)

                if label:
                    self.relation_index[label].append(idx)

        print(f"索引完成: {len(self.entity_index)} 个实体, {len(self.relation_index)} 种关系")

    def extract_entities(self, text: str) -> List[str]:
        """从文本中提取可能的实体"""
        if not text:
            return []

        # 使用jieba分词
        words = jieba.lcut(text)

        entities = []

        # 检查分词结果中的实体
        for word in words:
            if len(word) > 1 and word in self.entity_index and self._is_valid_entity(word):
                entities.append(word)

        # 检查完整文本是否匹配实体
        if text in self.entity_index and self._is_valid_entity(text):
            entities.append(text)

        # 检查文本片段（限制长度避免过度匹配）
        for i in range(len(text)):
            for j in range(i+2, min(i+10, len(text)+1)):  # 限制最大长度为10
                substring = text[i:j]
                if substring in self.entity_index and self._is_valid_entity(substring):
                    entities.append(substring)

        return list(set(entities))

    def search_by_entities(self, entities: List[str]) -> List[Dict]:
        """基于实体列表搜索相关知识"""
        if not entities or not self.loaded:
            return []

        record_scores = defaultdict(int)

        # 计算每个记录的相关性得分
        for entity in entities:
            if entity in self.entity_index:
                for record_idx in self.entity_index[entity]:
                    record_scores[record_idx] += 1

        # 按得分排序，返回top记录
        sorted_records = sorted(record_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for record_idx, score in sorted_records[:10]:  # 返回top 10
            record = self.kg_data[record_idx].copy()
            record['relevance_score'] = score
            results.append(record)

        return results

    def _is_valid_entity(self, entity: str) -> bool:
        """检查实体是否有效（人工质量过滤）"""
        if not entity or not entity.strip():
            return False

        entity = entity.strip()

        # 过滤单个字符（除了一些有意义的单字实体）
        if len(entity) == 1:
            valid_single_chars = {'中', '美', '欧', '亚', '东', '西', '南', '北', '新', '老', '大', '小', '高', '低', '上', '下', '内', '外', '前', '后'}
            return entity in valid_single_chars

        # 过滤纯标点符号
        import re
        if re.match(r'^[^\w\u4e00-\u9fa5]+$', entity):
            return False

        # 过滤纯空白字符
        if re.match(r'^\s+$', entity):
            return False

        # 过滤明显的片段（以常见字开头但很短的无意义组合）
        if len(entity) <= 2:
            meaningless_patterns = [
                r'^[的了在与和及或]',  # 介词、连词开头
                r'^[。，、；：！？\s]',  # 标点开头
                r'^[0-9]+$',  # 纯数字
                r'^\W+$',  # 纯符号
            ]
            for pattern in meaningless_patterns:
                if re.match(pattern, entity):
                    return False

        # 保留有意义的短实体
        if len(entity) <= 3:
            meaningful_short = {
                # 地名
                '北京', '上海', '广州', '深圳', '吉林', '内蒙', '山西', '陕西', '河北', '河南', '山东',
                '江苏', '浙江', '福建', '广东', '海南', '四川', '云南', '贵州', '湖北', '湖南', '江西',
                '安徽', '辽宁', '黑龙江', '天津', '重庆', '宁夏', '新疆', '西藏', '青海', '甘肃',
                # 机构
                '中科院', '清华', '北大', '中石油', '中石化', '中海油', '国电', '华能', '大唐',
                # 技术术语
                'CO2', 'CCS', 'CCUS', 'EOR', 'MEA', 'MDEA', 'PSA', 'TSA',
                # 基础词汇
                '技术', '项目', '公司', '企业', '政府', '政策', '标准', '设备', '环境', '能源',
                '工业', '研究', '开发', '建设', '管理', '服务', '系统', '方法', '过程', '材料',
                '产品', '市场', '投资', '合作', '发展', '应用', '科技', '创新', '数据', '信息',
                '碳捕集', '封存', '利用', '减排', '节能', '清洁', '绿色', '低碳', '零碳',
                '发电', '化工', '钢铁', '水泥', '石化', '煤化工', '电厂', '工厂', '装置',
                '管道', '储罐', '压缩', '输送', '注入', '监测', '安全', '成本', '效益'
            }
            return entity in meaningful_short

        # 长度大于3的实体，进行更严格的检查
        # 过滤以无意义字符结尾的实体
        if re.search(r'[。，、；：！？\s]+$', entity):
            return False

        # 过滤包含过多标点的实体
        punct_count = len(re.findall(r'[^\w\u4e00-\u9fa5]', entity))
        if punct_count > len(entity) * 0.3:  # 标点超过30%
            return False

        # 过滤以常见虚词开头的实体
        if re.match(r'^[而且但是或者因为所以如果然后当时这些那些一些每个各种不同相同类似]+', entity):
            return False

        # 过滤以数字结尾的奇怪组合
        if re.search(r'[^\d]\d+$', entity) and len(entity) < 8:  # 非数字+数字结尾且较短
            return False

        # 过滤包含换行符的实体
        if '\n' in entity:
            return False

        # 过滤明显的文本片段错误
        if re.match(r'^[的了在与和及或以及][^\w\u4e00-\u9fa5]', entity):
            return False

        return True

    def extract_subgraph(self, entities: List[str]) -> Dict:
        """提取以给定实体为中心的子图"""
        if not entities or not self.loaded:
            return {"nodes": [], "edges": []}

        nodes = set()
        edges = []

        # 收集相关记录
        relevant_records = self.search_by_entities(entities)

        for record in relevant_records:
            relations = record.get('relationMentions', [])

            for rel in relations:
                em1 = rel.get('em1Text', '')
                em2 = rel.get('em2Text', '')
                label = rel.get('label', '')

                # 应用实体质量过滤
                if (em1 and em2 and label and
                    self._is_valid_entity(em1) and self._is_valid_entity(em2)):

                    nodes.add(em1)
                    nodes.add(em2)

                    edges.append({
                        "source": em1,
                        "target": em2,
                        "relation": label,
                        "value": label,
                        "name": label,
                        "sentence": record.get('sentText', '')
                    })

        return {
            "nodes": [{"id": node, "name": node, "label": node} for node in nodes],
            "links": edges,
            "edges": edges  # 保持向后兼容
        }

    def search_knowledge(self, query: str) -> Tuple[List[Dict], Dict]:
        """搜索知识图谱，返回相关知识和子图"""
        if not self.loaded:
            return [], {"nodes": [], "edges": []}

        # 提取查询中的实体
        entities = self.extract_entities(query)
        print(f"提取的实体: {entities}")

        if not entities:
            # 如果没有直接匹配的实体，尝试关键词搜索
            entities = self._keyword_search(query)

        # 搜索相关知识
        knowledge = self.search_by_entities(entities)

        # 提取子图
        subgraph = self.extract_subgraph(entities)

        return knowledge, subgraph

    def _keyword_search(self, query: str) -> List[str]:
        """基于关键词搜索实体"""
        keywords = jieba.lcut(query)
        found_entities = []

        for keyword in keywords:
            if len(keyword) > 1:
                # 在实体中查找包含关键词的实体
                for entity in self.entity_index.keys():
                    if keyword in entity and entity not in found_entities:
                        found_entities.append(entity)

        return found_entities[:5]  # 返回前5个

    def format_knowledge_for_prompt(self, knowledge: List[Dict]) -> str:
        """格式化知识用于LLM prompt"""
        if not knowledge:
            return ""

        formatted = []
        for item in knowledge[:3]:  # 只取前3个最相关的
            relations = item.get('relationMentions', [])
            sentence = item.get('sentText', '')

            if relations:
                formatted.append(f"相关知识: {sentence}")

                for rel in relations[:3]:  # 每个记录最多3个关系
                    em1 = rel.get('em1Text', '')
                    em2 = rel.get('em2Text', '')
                    label = rel.get('label', '')

                    if em1 and em2 and label:
                        formatted.append(f"  {em1} - {label} - {em2}")

        return "\n".join(formatted)

    def get_statistics(self) -> Dict:
        """获取知识图谱统计信息"""
        if not self.loaded:
            return {}

        total_relations = sum(len(record.get('relationMentions', [])) for record in self.kg_data)

        return {
            "total_records": len(self.kg_data),
            "total_entities": len(self.entity_index),
            "total_relations": total_relations,
            "relation_types": len(self.relation_index)
        }