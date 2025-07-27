from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        for i in range(10):  # 模拟发送10条消息
            await asyncio.sleep(1)  # 模拟异步I/O操作
            yield f"data: Message {i}\n\n"  # SSE标准格式

    return EventSourceResponse(event_generator())

# pip install sse-starlette
# uvicorn sse_server:app --reload