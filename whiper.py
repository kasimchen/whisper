import os
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel

app = Flask(__name__)

try:
    # 初始化 Whisper 模型，指定使用 GPU
    model = WhisperModel("base.en", device="cuda", compute_type="float16")
    print("GPU 已成功启用并正常使用。")
except Exception as e:
    print(f"GPU 启用失败，将使用 CPU。错误信息: {e}")
    model = WhisperModel("base.en")


@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['file']

        # 检查文件名是否有效
        if audio_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # 保存上传的文件到临时目录
        temp_file_path = "temp_audio_file.mp3"
        audio_file.save(temp_file_path)

        # 进行音频转录
        segments, info = model.transcribe(temp_file_path, temperature=0.0)

        # 整理转录结果
        transcription = []
        current_result = None

        for segment in segments:
            if current_result is None:
                current_result = {
                    "start_time": "{:.2f}s".format(segment.start),
                    "end_time": "{:.2f}s".format(segment.end),
                    "text": segment.text
                }
            else:
                last_char = current_result["text"][-1] if current_result["text"] else None
                if last_char not in [".", "?"]:
                    # 如果当前句子最后一个字符不是句号也不是问号，拼接文本和时间
                    current_result["text"] += "" + segment.text
                    current_result["end_time"] = "{:.2f}s".format(segment.end)
                else:
                    # 如果当前句子最后一个字符是句号或问号，保存当前句子并开始新的句子
                    transcription.append(current_result)
                    current_result = {
                        "start_time": "{:.3f}".format(segment.start),
                        "end_time": "{:.3f}".format(segment.end),
                        "text": segment.text.strip()
                    }

        # 添加最后一个句子
        if current_result:
            transcription.append(current_result)

        # 删除临时文件
        os.remove(temp_file_path)

        return jsonify({
            "detected_language": info.language,
            "language_probability": info.language_probability,
            "transcription": transcription
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
