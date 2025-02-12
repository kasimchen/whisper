import os
from faster_whisper import WhisperModel

try:
    # 初始化 Whisper 模型，指定使用 GPU
    model = WhisperModel("base.en", device="cuda", compute_type="float16")
    print("GPU 已成功启用并正常使用。")
except Exception as e:
    print(f"GPU 启用失败，将使用 CPU。错误信息: {e}")
    model = WhisperModel("base.en")