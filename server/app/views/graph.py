import os
import json
from flask import request, Blueprint, jsonify
from thefuzz import process


mod = Blueprint('graph', __name__, url_prefix='/graph')


@mod.route('/', methods=['GET'])
def graph():
    # Load CCUS knowledge graph data
    ccus_data_path = '../data/ccus_project/base.json'
    if os.path.exists(ccus_data_path):
        with open(ccus_data_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            data = [json.loads(line.strip()) for line in lines if line.strip()]
    else:
        data = {"error": "CCUS knowledge graph data not found"}

    return jsonify({
        'data': data,
        'message': 'CCUS Knowledge Graph Loaded!'
    })


# @mod.route('/search', methods=['GET'])
# def get_triples():
#     # 获取参数
#     user_input = request.args.get('search')
#     result = search_node_item(user_input)

#     return jsonify({
#         'data': result,
#         'message': 'Got it!'
#     })
