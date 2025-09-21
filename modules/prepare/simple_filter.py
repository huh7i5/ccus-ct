import re
import jieba

def simple_tokenize(text):
    """简单的中文分词，不依赖transformers"""
    # 使用jieba分词
    tokens = list(jieba.cut(text))
    return tokens

def auto_filter(items, model_name_or_path=None):
    """用于自动过滤到一些错误的三元组，简化版本不依赖transformers

    Args:
        items (数组): 所有的实例，每个实例是一个字典，包含了句子、实体、关系
        model_name_or_path (字符串): 预训练模型的名字或者路径（忽略，保持接口兼容）

    Returns:
        过滤后的 items
    """

    for example in items:
        sent_text = example["sentText"]
        sent_tokens = simple_tokenize(sent_text)

        relations = []
        for relation in example["relationMentions"]:
            sub_text = relation["em1Text"]
            obj_text = relation["em2Text"]

            sub_tokens = simple_tokenize(sub_text)
            obj_tokens = simple_tokenize(obj_text)

            if len(sub_tokens) == 0 or len(obj_tokens) == 0:
                continue

            if len(sub_tokens) > 15 or len(obj_tokens) > 15:
                continue

            # 简单检查实体是否在句子中
            if sub_text not in sent_text or obj_text not in sent_text:
                continue

            # 1. 判断 subject 是否在句子中
            sub_start = -1
            sub_end = -1
            for i in range(len(sent_tokens) - len(sub_tokens) + 1):
                if sent_tokens[i:i+len(sub_tokens)] == sub_tokens:
                    sub_start = i
                    sub_end = i + len(sub_tokens) - 1
                    break

            # 如果找不到，尝试字符串匹配
            if sub_start == -1:
                if sub_text in sent_text:
                    sub_start = 0  # 简化处理
                    sub_end = 0
                else:
                    continue

            # 2. 判断 object 是否在句子中
            obj_start = -1
            obj_end = -1
            for i in range(len(sent_tokens) - len(obj_tokens) + 1):
                if sent_tokens[i:i+len(obj_tokens)] == obj_tokens:
                    obj_start = i
                    obj_end = i + len(obj_tokens) - 1
                    break

            # 如果找不到，尝试字符串匹配
            if obj_start == -1:
                if obj_text in sent_text:
                    obj_start = 0  # 简化处理
                    obj_end = 0
                else:
                    continue

            relations.append({
                "em1Text": relation["em1Text"],
                "em2Text": relation["em2Text"],
                "label": relation["label"],
                "em1Start": sub_start,
                "em1End": sub_end,
                "em2Start": obj_start,
                "em2End": obj_end
            })

        example["relationMentions"] = relations

    return items