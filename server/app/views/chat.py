import os
import json
from flask import Response, request, Blueprint, jsonify

# Skip model dependency for testing
# from app.utils.chat_glm import stream_predict

mod = Blueprint('chat', __name__, url_prefix='/chat')


@mod.route('/', methods=['GET'])
def chat_get():
    return "CCUS Knowledge Graph Chat API Ready!"


@mod.route('/', methods=['POST'])
def chat():
    try:
        request_data = json.loads(request.data)
        prompt = request_data['prompt']
        history = request_data.get('history', [])

        # Simple response for testing without model
        response = {
            "query": prompt,
            "response": f"CCUS知识图谱系统收到查询: {prompt}. 模型功能正在测试中。",
            "history": history + [(prompt, f"收到关于CCUS的查询: {prompt}")],
            "graph": {},
            "wiki": {"title": "CCUS测试", "summary": "碳捕集利用与封存技术测试"}
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
