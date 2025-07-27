from fastapi import FastAPI
import asyncio

app = FastAPI()

# 异步函数模拟数据库查询
async def database_query():
    await asyncio.sleep(5)  # 模拟I/O操作，例如数据库查询
    return {"result": "database response"}

# 异步函数模拟外部API调用
async def external_api_call():
    await asyncio.sleep(5)  # 模拟I/O操作，例如API请求
    return {"result": "external api response"}

@app.get("/items/")
async def read_items():
    # 记录开始时间
    start_time = asyncio.get_event_loop().time()
    
    # 同时启动两个异步任务
    db_task = asyncio.create_task(database_query())
    api_task = asyncio.create_task(external_api_call())

    # 等待两个异步任务完成
    db_result = await db_task
    api_result = await api_task

    # 记录结束时间并计算总耗时
    end_time = asyncio.get_event_loop().time()
    total_time = end_time - start_time

    # 合并结果并返回
    return {
        "database": db_result, 
        "external_api": api_result,
        "start_time": start_time,
        "end_time": end_time,
        "total_time": f"{total_time:.2f} seconds"
    }


# uvicorn async_demo:app --reload