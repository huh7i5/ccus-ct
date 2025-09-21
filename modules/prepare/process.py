import os
from data.schema import ccus_schema

# 使用基于规则的替代方案，而不是PaddleNLP UIE
try:
    # 尝试导入PaddleNLP（如果可用）
    from paddle import inference as paddle_infer
    from paddlenlp import Taskflow
    PADDLE_AVAILABLE = True

    # 定义一个函数，用于关系抽取
    def paddle_relation_ie(content):
        relation_ie = Taskflow("information_extraction", schema=ccus_schema.schema, batch_size=2)
        return relation_ie(content)

    # 关系抽取并修改json文件
    def rel_json(content):
        all_relations = [] # 定义一个空列表，用于存储每个chapter的关系信息
        res_relation = paddle_relation_ie(content)  # 传入文本进行关系识别
        for rel in res_relation:
            for sub_type, sub_rel in rel.items():
                for sub in sub_rel:
                    if sub.get("relations") is None:
                        continue
                    for rel_type, rel_obj in sub["relations"].items():
                        for obj in rel_obj:
                            if not sub['text'] or not obj['text']:
                                continue
                            rel_triple = {"em1Text": sub['text'],"em2Text": obj['text'],"label": rel_type}
                            all_relations.append(rel_triple)
        return all_relations

except ImportError:
    PADDLE_AVAILABLE = False
    print("PaddleNLP not available, using rule-based alternative")

    # 导入替代方案
    from .alternative_process import rule_based_relation_extraction

    def rel_json(content):
        return rule_based_relation_extraction(content)


# 执行函数
def uie_execute(texts):
    if not PADDLE_AVAILABLE:
        print("Using rule-based relation extraction as PaddleNLP fallback")

    sent_id = 0
    all_items = []
    for line in texts:
        line = line.strip()
        if not line:
            continue

        all_relations = rel_json(line)

        item = {}
        item["id"] = sent_id
        item["sentText"] = line
        item["relationMentions"] = all_relations

        sent_id += 1
        if sent_id % 10 == 0 and sent_id != 0:
            print("Done {} lines".format(sent_id))

        all_items.append(item)

    return all_items
