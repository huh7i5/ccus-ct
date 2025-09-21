import os
from app import apps

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 启用ChatGLM模型
from app.utils.chat_glm import start_model


if __name__ == '__main__':
    print("🚀 启动CCUS知识图谱+大模型服务器...")

    # 启动ChatGLM模型
    model_loaded = start_model()

    if model_loaded:
        print("✅ ChatGLM-6B模型加载成功，启动完整服务")
    else:
        print("⚠️ ChatGLM-6B模型加载失败，启动基础服务")

    apps.secret_key = os.urandom(24)
    print("🌐 服务器启动在 http://0.0.0.0:8000")
    apps.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

