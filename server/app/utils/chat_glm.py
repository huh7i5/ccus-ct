import os
import sys
import json
import torch
from pathlib import Path
from opencc import OpenCC
from transformers import AutoTokenizer, AutoModel
from app.utils.image_searcher import ImageSearcher
from app.utils.query_wiki import WikiSearcher
from app.utils.ner import Ner
from app.utils.graph_utils import convert_graph_to_triples, search_node_item
from app.utils.ccus_kg_search import CCUSKnowledgeGraphSearcher

# 全局变量
model = None
tokenizer = None
init_history = None

# 初始化各种工具
ner = Ner()
image_searcher = ImageSearcher()
wiki_searcher = WikiSearcher()
ccus_searcher = CCUSKnowledgeGraphSearcher()
cc = OpenCC('t2s')

# 模型路径配置
MODEL_PATHS = [
    "/root/KnowledgeGraph-based-on-Raw-text-A27-main/KnowledgeGraph-based-on-Raw-text-A27-main/models/chatglm-6b",
    "./models/chatglm-6b",
    "THUDM/chatglm-6b"
]

def predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history
    return model.chat(tokenizer, user_input, history)


def stream_predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history

    ref = ""

    # 1. CCUS知识图谱检索
    print(f"🔍 CCUS知识图谱检索: {user_input}")
    knowledge, subgraph = ccus_searcher.search_knowledge(user_input)

    if knowledge:
        kg_info = ccus_searcher.format_knowledge_for_prompt(knowledge)
        if kg_info:
            ref += f"CCUS知识图谱信息：\n{kg_info}\n\n"
            print(f"找到CCUS知识: {len(knowledge)} 条相关记录")

    # 2. 实体识别（保留原有逻辑）
    graph = subgraph if subgraph["nodes"] else {}
    entities = []

    try:
        entities = ner.get_entities(user_input, etypes=["技术", "项目", "机构", "地理", "政策", "标准", "经济", "设备", "指标", "环境"])
        print("识别的实体: ", entities)
    except:
        # 如果实体识别失败，使用CCUS搜索器的实体提取
        entities = ccus_searcher.extract_entities(user_input)
        print("CCUS实体提取: ", entities)

    # 3. 传统三元组检索（作为补充）
    triples = []
    for entity in entities:
        try:
            entity_graph = search_node_item(entity, graph if graph else None)
            if entity_graph:
                triples += convert_graph_to_triples(entity_graph, entity)
        except:
            pass

    if triples:
        triples_str = ""
        for t in triples:
            triples_str += f"({t[0]} {t[1]} {t[2]})；"
        ref += f"补充三元组信息：{triples_str}\n\n"

    # 4. 图像搜索
    image = None
    try:
        image = image_searcher.search(user_input)
    except:
        image = None

    # 5. 外部知识搜索（Wikipedia等）
    wiki = None
    try:
        for ent in entities + [user_input]:
            wiki = wiki_searcher.search(ent)
            if wiki is not None:
                break

        # 将Wikipedia搜索到的繁体转为简体
        if wiki:
            ref += f"外部知识：{cc.convert(wiki.summary)}\n"
            wiki = {
                "title": cc.convert(wiki.title),
                "summary": cc.convert(wiki.summary),
            }
            print("找到Wikipedia信息:", wiki["title"])
    except Exception as e:
        print(f"Wikipedia搜索失败: {e}")

    if not wiki:
        wiki = {
            "title": "CCUS技术知识",
            "summary": "基于CCUS领域知识图谱的专业问答",
        }

    if model is not None:
        if ref:
            chat_input = f"\n===参考资料===：\n{ref}；\n\n根据上面资料，用简洁且准确的话回答下面问题：\n{user_input}"
        else:
            chat_input = user_input

        clean_history = []
        for user_input, response in history:
            if "===参考资料===" in user_input:
                user_input = user_input.split("===参考资料===")[0]
            clean_history.append((user_input, response))

        print("chat_input: ", chat_input)
        for response, history in model.stream_chat(tokenizer, chat_input, clean_history):
            updates = {}
            for query, response in history:
                updates["query"] = query
                updates["response"] = response

            result = {
                "history": history,
                "updates": updates,
                "image": image,
                "graph": graph,
                "wiki": wiki
            }
            yield json.dumps(result, ensure_ascii=False).encode('utf8') + b'\n'

    else:
        updates = {
            "query": user_input,
            "response": "模型加载中，请稍后再试"
        }

        result = {
            "history": history,
            "updates": updates,
            "image": image,
            "graph": graph,
            "wiki": wiki
        }
        yield json.dumps(result, ensure_ascii=False).encode('utf8') + b'\n'

# 加载模型
def start_model():
    global model, tokenizer, init_history

    print("🤖 正在加载ChatGLM-6B模型...")

    # 尝试各个可能的模型路径
    model_path = None
    for path in MODEL_PATHS:
        if os.path.exists(path) or path.startswith("THUDM/"):
            model_path = path
            print(f"找到模型路径: {path}")
            break

    if not model_path:
        print("❌ 未找到ChatGLM-6B模型，请先下载")
        print("运行: python download_chatglm.py")
        return False

    try:
        from transformers import AutoTokenizer, AutoModel
        # 加载tokenizer
        print("加载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

        # 加载模型
        print("加载模型权重...")
        if torch.cuda.is_available():
            model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
            print("✅ 模型已加载到GPU")
        else:
            model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
            print("⚠️ 模型加载到CPU (性能较慢)")

        model.eval()

        # 初始化对话历史
        pre_prompt = "你叫 ChatKG，是一个专业的CCUS（碳捕集利用与封存）领域知识图谱问答机器人。你可以基于CCUS领域知识图谱回答相关技术问题。"
        _, history = predict(pre_prompt, [])
        init_history = history

        print("✅ ChatGLM-6B模型加载成功！")
        return True

    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        print("尝试自动下载模型...")

        # 尝试自动下载
        try:
            from transformers import AutoTokenizer, AutoModel
            print("从Hugging Face下载ChatGLM-6B...")

            tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
            if torch.cuda.is_available():
                model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
            else:
                model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)

            model.eval()

            # 保存模型到本地
            local_path = "./models/chatglm-6b"
            os.makedirs(local_path, exist_ok=True)
            tokenizer.save_pretrained(local_path)
            model.save_pretrained(local_path)

            print(f"✅ 模型下载并保存到: {local_path}")

            # 初始化对话历史
            pre_prompt = "你叫 ChatKG，是一个专业的CCUS（碳捕集利用与封存）领域知识图谱问答机器人。你可以基于CCUS领域知识图谱回答相关技术问题。"
            _, history = predict(pre_prompt, [])
            init_history = history

            return True

        except Exception as e2:
            print(f"❌ 自动下载也失败: {e2}")
            print("请手动下载ChatGLM-6B模型")
            return False