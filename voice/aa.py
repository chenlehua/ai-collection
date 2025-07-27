import asyncio
import websockets
import base64
import tempfile
import os
import json
import soundfile as sf
from voice_assistant_core import VoiceAssistant
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
import uvicorn

app = FastAPI()

# 挂载前端静态页面
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# 初始化语音助手核心
assistant = VoiceAssistant(wake_word="小助手")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()

            # 写入临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name

            # 解码为PCM
            try:
                wav_data, samplerate = sf.read(tmp_path)
                if assistant.detect_wake_word(wav_data, samplerate):
                    await websocket.send_text(json.dumps({"status": "✅ 唤醒成功，处理中..."}))
                    text = assistant.transcribe(wav_data, samplerate)
                    reply = assistant.chat(text)
                    tts_path = assistant.text_to_speech(reply)
                    await websocket.send_text(json.dumps({"audio_url": f"/audio/{os.path.basename(tts_path)}"}))
                else:
                    await websocket.send_text(json.dumps({"status": "🎧 监听中..."}))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
            finally:
                os.remove(tmp_path)

    except WebSocketDisconnect:
        print("WebSocket 客户端断开")

# 音频文件服务
app.mount("/audio", StaticFiles(directory="audio_cache"), name="audio")

if __name__ == "__main__":
    os.makedirs("audio_cache", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
