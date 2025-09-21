import re
import json
from typing import List, Dict, Any
from data.schema import ccus_schema

def rule_based_relation_extraction(text: str) -> List[Dict]:
    """
    基于规则的关系抽取，替代PaddleNLP UIE
    针对CCUS领域的实体和关系抽取
    """
    all_relations = []

    # 获取schema中的实体类型和关系类型
    entity_types = list(ccus_schema.schema.keys())

    # 基本的实体识别模式
    entity_patterns = {
        "技术": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:技术|工艺|方法|装置|设备)",
            r"(?:CO2|二氧化碳)(?:捕集|封存|利用|运输|转化)",
            r"(?:CCUS|CCS|CCU|DAC|BECCS)"
        ],
        "项目": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:项目|工程|示范|基地|园区)",
            r"(?:示范|试点|商业化|产业化)(?:项目|工程|基地)"
        ],
        "机构": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:公司|企业|集团|研究院|大学|中心|实验室)",
            r"(?:中石油|中石化|中海油|华能|大唐|国电|华电|中核|中广核)"
        ],
        "地理": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:省|市|县|区|盆地|油田|气田|矿区)",
            r"(?:胜利|大庆|塔里木|鄂尔多斯|渤海湾|松辽|四川)(?:盆地|油田|气田)?"
        ],
        "政策": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:政策|法规|标准|规范|办法|条例|通知|意见)",
            r"(?:碳达峰|碳中和|双碳|减排|低碳)(?:政策|目标|战略|规划)?"
        ],
        "经济": [
            r"\d+(?:\.\d+)?(?:亿|万|千)?(?:元|美元|欧元)",
            r"(?:投资|成本|收益|利润|价格|费用).*?\d+",
            r"\d+(?:\.\d+)?(?:元/吨|美元/吨)"
        ],
        "设备": [
            r"[a-zA-Z0-9\u4e00-\u9fa5]+(?:设备|装置|机组|系统|管道|储罐|压缩机|泵)",
            r"(?:捕集|分离|净化|压缩|运输|封存|监测)(?:设备|装置|系统)"
        ],
        "指标": [
            r"\d+(?:\.\d+)?(?:%|％|万吨|吨|立方米|兆瓦|千瓦)",
            r"(?:效率|容量|规模|产能|处理能力).*?\d+",
            r"(?:捕集|封存|利用|减排)(?:率|量|效率).*?\d+"
        ]
    }

    # 关系抽取模式
    relation_patterns = [
        # 技术应用关系
        (r"([^，。；！？\s]+)(?:采用|应用|使用)([^，。；！？\s]+(?:技术|工艺|方法))", "技术应用"),
        # 项目投资关系
        (r"([^，。；！？\s]+)(?:投资|出资|资助)([^，。；！？\s]+(?:项目|工程))", "投资关系"),
        # 地理位置关系
        (r"([^，。；！？\s]+(?:项目|工程|基地))(?:位于|建在|坐落在)([^，。；！？\s]+(?:省|市|县|区))", "位于"),
        # 机构合作关系
        (r"([^，。；！？\s]+(?:公司|企业|机构))(?:与|和)([^，。；！？\s]+(?:公司|企业|机构))(?:合作|联合)", "合作关系"),
        # 技术指标关系
        (r"([^，。；！？\s]+(?:技术|工艺))(?:的)?([^，。；！？\s]*(?:效率|容量|能力))(?:达到|为|是)([^，。；！？\s]*\d+[^，。；！？\s]*)", "技术指标"),
        # 设备组成关系
        (r"([^，。；！？\s]+(?:系统|装置))(?:包括|含有|由)([^，。；！？\s]+(?:设备|装置|部件))", "组成关系"),
    ]

    # 提取实体
    entities = {}
    for entity_type, patterns in entity_patterns.items():
        entities[entity_type] = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity_text = match.group().strip()
                if len(entity_text) > 1 and entity_text not in entities[entity_type]:
                    entities[entity_type].append(entity_text)

    # 提取关系
    for pattern, relation_type in relation_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match.groups()) >= 2:
                entity1 = match.group(1).strip()
                entity2 = match.group(2).strip()

                if len(entity1) > 1 and len(entity2) > 1:
                    relation = {
                        "em1Text": entity1,
                        "em2Text": entity2,
                        "label": relation_type
                    }
                    all_relations.append(relation)

    # 基于schema生成一些基本关系
    for entity_type, relation_list in ccus_schema.schema.items():
        type_entities = entities.get(entity_type, [])
        for entity in type_entities[:3]:  # 限制每种类型最多3个实体，避免过多
            for relation_name in relation_list[:5]:  # 限制每个实体最多5个关系
                # 寻找可能的关系对象
                for target_type, target_entities in entities.items():
                    if target_type != entity_type and target_entities:
                        target_entity = target_entities[0]  # 取第一个作为示例
                        relation = {
                            "em1Text": entity,
                            "em2Text": target_entity,
                            "label": relation_name
                        }
                        all_relations.append(relation)
                        break  # 每个关系只添加一个示例

    return all_relations

def alternative_uie_execute(texts: List[str]) -> List[Dict]:
    """
    替代UIE执行函数
    """
    sent_id = 0
    all_items = []

    for line in texts:
        line = line.strip()
        if not line:
            continue

        all_relations = rule_based_relation_extraction(line)

        item = {
            "id": sent_id,
            "sentText": line,
            "relationMentions": all_relations
        }

        sent_id += 1
        if sent_id % 10 == 0:
            print(f"Processed {sent_id} lines")

        all_items.append(item)

    return all_items

# 为了保持兼容性，提供与原始模块相同的接口
def uie_execute(texts: List[str]) -> List[Dict]:
    """
    保持与原始process.py模块的接口兼容性
    """
    return alternative_uie_execute(texts)