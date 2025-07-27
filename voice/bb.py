#  apt install ffmpeg
# pip install git+https://github.com/openai/whisper.git
# pip install openai-whisper



import whisper
import tempfile
import os

class LocalWhisperASR:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)  # 可选 tiny, base, small, medium, large

    def transcribe(self, audio_bytes: bytes, suffix=".wav") -> str:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name

        try:
            result = self.model.transcribe(temp_path, language="zh")
            return result["text"]
        finally:
            os.remove(temp_path)





from your_module.local_whisper import LocalWhisperASR

asr = LocalWhisperASR(model_size="base")  # 可改成 "medium" 等
text = asr.transcribe(audio_bytes)

