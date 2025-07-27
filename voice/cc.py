import os
import tempfile
import asyncio
import json
import soundfile as sf
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
from TTS.api import TTS
import torch
import whisper

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化 TTS 和 Whisper 本地模型
tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC", progress_bar=False, gpu=torch.cuda.is_available())
asr_model = whisper.load_model("base")

WAKE_WORDS = ["小语"]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()

            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name

            pcm_path = tmp_path.replace(".webm", ".wav")
            os.system(f"ffmpeg -i {tmp_path} -ar 16000 -ac 1 -f wav {pcm_path} -y")

            # 自动语音识别
            result = asr_model.transcribe(pcm_path)
            text = result["text"].strip()

            print("识别内容:", text)

            if not any(w in text for w in WAKE_WORDS):
                await websocket.send_text(json.dumps({"status": "👂 未检测到唤醒词，继续监听..."}))
                continue

            # 清理唤醒词文本
            for w in WAKE_WORDS:
                text = text.replace(w, "")

            # 生成回复语音
            reply_text = f"你好，我是语音助手，你刚刚说的是：{text.strip()}"

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tts_file:
                tts.tts_to_file(text=reply_text, file_path=tts_file.name)
                reply_path = tts_file.name

            # 返回语音文件的 URL
            audio_url = f"/static/{os.path.basename(reply_path)}"
            os.rename(reply_path, f"static/{os.path.basename(reply_path)}")

            await websocket.send_text(json.dumps({"audio_url": audio_url}))

    except WebSocketDisconnect:
        print("连接断开")
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
