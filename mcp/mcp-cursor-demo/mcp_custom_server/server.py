# server.py
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uvicorn
from config import API_KEY
from typing import List
from decimal import Decimal, getcontext

getcontext().prec = 50

app = FastAPI(
    title="Calculator MCP Server",
    description="一个简单的带安全认证的计算器 MCP 服务端",
    version="1.0.0"
)

# API key security scheme
api_key_header = APIKeyHeader(name="X-Api-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """验证 API 密钥"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

class Numbers(BaseModel):
    """数字输入模型"""
    num1: float
    num2: float

class Result(BaseModel):
    """计算结果模型"""
    result: float

@app.post(
    "/add",
    response_model=Result,
    summary="Addition Service",
    description="计算两个数的和",
    operation_id="add_numbers"
)
async def add_numbers(
    numbers: Numbers,
    api_key: str = Depends(verify_api_key)
) -> Result:
    """计算两个数的和"""
    return Result(result=numbers.num1 + numbers.num2)

@app.get(
    "/capabilities",
    summary="获取服务能力",
    operation_id="get_capabilities"
)
async def get_capabilities():
    """返回服务能力描述"""
    return {
        "add": {
            "name": "Addition Service",
            "description": "计算两个数的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "第一个数"
                    },
                    "num2": {
                        "type": "number",
                        "description": "第二个数"
                    }
                },
                "required": ["num1", "num2"]
            },
            "security": {
                "api_key": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-Api-Key"
                }
            }
        }
    }

@app.get(
    "/",
    summary="API Root",
    description="Returns basic information about the API",
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
            "/add",
            "/capabilities"
        ],
        "mcp": {
            "version": "0.1.0",
            "capabilities": [
                "add"
            ]
        }
    }

@app.post(
    "/",
    summary="Root POST Handler",
    description="Handles POST requests to root path",
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
                "add"
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)