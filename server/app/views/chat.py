import os
import json
from flask import Response, request, Blueprint, jsonify

from app.utils.chat_glm import stream_predict

mod = Blueprint('chat', __name__, url_prefix='/api')


@mod.route('/', methods=['GET'])
def chat_get():
    return "CCUS Knowledge Graph Chat API Ready!"


@mod.route('/chat', methods=['POST'])
def chat():
    try:
        request_data = json.loads(request.data)
        prompt = request_data['prompt']
        history = request_data.get('history', [])

        # 使用流式预测返回响应
        def generate():
            for response_chunk in stream_predict(prompt, history):
                yield response_chunk

        return Response(generate(), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 400
