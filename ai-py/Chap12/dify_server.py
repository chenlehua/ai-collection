from fastapi import FastAPI, Body, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    point: str
    params: dict = {}


@app.post("/api/dify/receive")
async def dify_receive(data: InputData = Body(...), authorization: str = Header(None)):
    """
    从 Dify 接收 API 查询数据。
    """
    expected_api_key = "123456"  # TODO 在此填入你的 API 密钥
    auth_scheme, _, api_key = authorization.partition(' ')

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    point = data.point

    # for debug
    print(f"point: {point}")

    if point == "ping":
        return {
            "result": "pong"
        }
    if point == "app.external_data_tool.query":
        return handle_app_external_data_tool_query(params=data.params)
    # elif point == "{point name}":
        # TODO 在此实现其他端点的处理逻辑

    raise HTTPException(status_code=400, detail="Not implemented")


def handle_app_external_data_tool_query(params: dict):
    app_id = params.get("app_id")
    tool_variable = params.get("tool_variable")
    inputs = params.get("inputs")
    query = params.get("query")

    # for debug
    print(f"app_id: {app_id}")
    print(f"tool_variable: {tool_variable}")
    print(f"inputs: {inputs}")
    print(f"query: {query}")

    # TODO 在此实现你的外部数据工具查询逻辑
    # 返回值必须是一个包含 "result" 键的字典，其值为查询结果
    if inputs.get("location") == "珠海":
        return {
            "result": "城市: 珠海\n温度: 10°C\n体感温度: 8°C\n空气质量: 差\n风向: 东北偏东\n风速: "
                      "8 公里/小时\n阵风: 14 公里/小时\n降水: 小雨"
        }
    else:
        return {"result": "未知城市"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)