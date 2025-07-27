# voice_assistant_core.py
import os
import time
import uuid
import tempfile
import soundfile as sf
import openai  # 用于调用 Whisper 或 ChatGPT
from TTS.api import TTS  # 使用 Coqui TTS

class VoiceAssistant:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC", progress_bar=False, gpu=False)
        self.wake_word = "小助手"

    def save_audio(self, audio_data: bytes, file_path: str):
        # 将 WebM 或 WAV 流保存成音频文件（这里假设是 WAV）
        with open(file_path, 'wb') as f:
            f.write(audio_data)

    def detect_wake_word(self, text: str) -> bool:
        return self.wake_word in text

    def transcribe(self, wav_path: str) -> str:
        # 也可以使用 whisper
        result = openai.Audio.transcribe("whisper-1", open(wav_path, "rb"))
        return result["text"]

    def reply(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def synthesize(self, text: str, out_path: str):
        self.tts.tts_to_file(text=text, file_path=out_path)

    def process_audio(self, audio_data: bytes) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "input.wav")
            out_path = os.path.join("audio_responses", f"{uuid.uuid4().hex}.wav")

            self.save_audio(audio_data, wav_path)
            transcript = self.transcribe(wav_path)

            if not self.detect_wake_word(transcript):
                return ""  # 未唤醒

            reply_text = self.reply(transcript)
            self.synthesize(reply_text, out_path)

            return out_path
