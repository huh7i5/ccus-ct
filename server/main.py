import os
from app import apps

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Skip model loading for testing
# from app.utils.chat_glm import start_model


if __name__ == '__main__':
    print("Starting CCUS Knowledge Graph Server...")
    print("Skipping model loading for testing purposes")
    apps.secret_key = os.urandom(24)
    apps.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

