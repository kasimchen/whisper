import os
from faster_whisper import WhisperModel
from huggingface_hub import hf_hub_download

# 定义模型名称和存储路径
model_name = "guillaumekln/faster-whisper-base.en"
model_file = "model.bin"
# 下载模型文件到本地
local_model_path = hf_hub_download(repo_id=model_name, filename=model_file,local_dir="model")

print(local_model_path)

try:
    # 初始化 Whisper 模型，指定使用 GPU
    model = WhisperModel("base.en", device="cuda", compute_type="float16")
    print("GPU 已成功启用并正常使用。")
except Exception as e:
    print(f"GPU 启用失败，将使用 CPU。错误信息: {e}")
    model = WhisperModel("base.en")



    