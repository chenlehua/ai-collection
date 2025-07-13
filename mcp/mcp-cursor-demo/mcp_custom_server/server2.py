# server.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn
from decimal import Decimal, getcontext # 导入 Decimal 模块以支持高精度计算

# 设置 Decimal 的全局精度，例如 50 位有效数字
getcontext().prec = 50

app = FastAPI(
    title="High-Precision Division MCP Server",
    description="一个提供高精度除法功能的 MCP 服务端，不带安全认证。",
    version="1.0.0"
)

# 定义请求体模型
class Numbers(BaseModel):
    """数字输入模型"""
    num1: Decimal # 使用 Decimal 类型进行高精度浮点数处理
    num2: Decimal

# 定义响应体模型
class Result(BaseModel):
    """计算结果模型"""
    result: Decimal

@app.post(
    "/divide",
    response_model=Result,
    summary="Division Service",
    description="计算两个数的高精度除法",
    operation_id="divide_numbers"
)
async def divide_numbers(
    numbers: Numbers
) -> Result:
    """计算两个数的高精度除法，并处理除数为零的情况"""
    if numbers.num2 == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="除数不能为零"
        )
    # 执行高精度除法
    return Result(result=numbers.num1 / numbers.num2)

@app.get(
    "/capabilities",
    summary="获取服务能力",
    description="返回服务能力描述，遵循 MCP 协议标准。",
    operation_id="get_capabilities"
)
async def get_capabilities():
    """返回服务能力描述"""
    return {
        "divide": {
            "name": "High-Precision Division Service",
            "description": "计算两个数的高精度除法。",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "被除数"
                    },
                    "num2": {
                        "type": "number",
                        "description": "除数"
                    }
                },
                "required": ["num1", "num2"]
            },
            # 由于不带认证，这里不需要 security 字段
        }
    }

@app.get(
    "/",
    summary="API Root",
    description="返回 API 的基本信息，包括名称、描述、版本和可用端点。",
    operation_id="get_root"
)
async def get_root():
    """返回 API 基本信息"""
    return {
        "name": app.title,
        "description": app.description,
        "version": app.version,
        "endpoints": [
            "/",
            "/divide",
            "/capabilities"
        ],
        "mcp": {
            "version": "0.1.0",
            "capabilities": [
                "divide"
            ]
        }
    }

@app.post(
    "/",
    summary="Root POST Handler",
    description="处理根路径的 POST 请求，返回成功状态和 MCP 能力信息。",
    operation_id="post_root"
)
async def post_root():
    """处理根路径的 POST 请求"""
    return {
        "status": "success",
        "message": "POST request received",
        "mcp": {
            "version": "0.1.0",
            "capabilities": [
                "divide"
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)