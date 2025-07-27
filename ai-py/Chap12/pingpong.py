from fastapi import FastAPI, Body, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    point: str
    params: dict = {}

@app.post("/api/dify/receive")
async def dify_receive(data: InputData = Body(...), authorization: str = Header(None)):
    """
    接收来自 Dify 的 API 请求
    """
    # 验证 API key
    expected_api_key = "123456"  # 替换为你的 API key
    
    if authorization:
        auth_scheme, _, api_key = authorization.partition(' ')
        if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
            raise HTTPException(status_code=401, detail="未授权访问")
    
    print(f"data.point: {data.point}")

    # 处理 ping 请求
    if data.point == "ping":
        return {
            "result": "pong"
        }
    
    # 处理天气查询请求
    if data.point == "app.external_data_tool.query":
        location = data.params.get("inputs", {}).get("location")
        if not location:
            raise HTTPException(status_code=400, detail="缺少location参数")
            
        # 这里模拟天气数据返回，实际使用时需要替换为真实的天气API调用
        weather_info = f"""City: {location}
Temperature: 20°C
RealFeel®: 22°C
Air Quality: Good
Wind Direction: NE
Wind Speed: 10 km/h
Wind Gusts: 15 km/h
Precipitation: None"""
        
        return {
            "result": weather_info
        }
    
    # 处理其他类型的请求
    raise HTTPException(status_code=400, detail="未实现的请求类型")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
