import os
import asyncio
import tempfile
import numpy as np
import whisper
import openai
import edge_tts
import websockets
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn


app = FastAPI()

class VoiceAssistant:
    def __init__(self):
        self.asr_model = whisper.load_model("base")

    def transcribe_audio(self, wav_path):
        result = self.asr_model.transcribe(wav_path, language="zh")
        return result.get("text", "")

    def ask_gpt(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"GPT请求失败：{e}"

    async def tts_to_url(self, text):
        communicate = edge_tts.Communicate(text=text, voice="zh-CN-XiaoxiaoNeural")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            output_path = tmpfile.name
        await communicate.save(output_path)
        return output_path

assistant = VoiceAssistant()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    audio_bytes = await websocket.receive_bytes()
    print("b")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name


    print("a")

    user_text = assistant.transcribe_audio(temp_audio_path)
    reply = assistant.ask_gpt(user_text)
    tts_path = await assistant.tts_to_url(reply)

    audio_url = f"/static/{os.path.basename(tts_path)}"
    os.makedirs("static", exist_ok=True)
    os.rename(tts_path, f"static/{os.path.basename(tts_path)}")

    await websocket.send_text(json.dumps({"audio_url": audio_url}))

if __name__ == "__main__":
    uvicorn.run("voice_assistant:app", host="0.0.0.0", port=7860, reload=False)
