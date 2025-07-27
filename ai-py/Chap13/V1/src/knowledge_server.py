from fastapi import FastAPI, Body, HTTPException, Header, Request
from pydantic import BaseModel
from typing import List, Dict, Optional

# 常量定义
EXPECTED_API_KEY = "123456"  # TODO: 替换为实际的 API 密钥

# 错误码定义
class ErrorCode:
    INVALID_AUTH = 1001
    AUTH_FAILED = 1002
    KNOWLEDGE_NOT_FOUND = 2001

# 错误信息定义
class ErrorMessage:
    MISSING_AUTH = "缺少 Authorization 头"
    INVALID_AUTH_FORMAT = "无效的 Authorization 头格式。预期格式为 'Bearer '"
    AUTH_FAILED = "授权失败"
    KNOWLEDGE_NOT_FOUND = "知识库不存在"

# 数据模型
class RetrievalSetting(BaseModel):
    top_k: int
    score_threshold: float

class InputData(BaseModel):
    knowledge_id: str
    query: str
    retrieval_setting: RetrievalSetting

class SearchResult(BaseModel):
    content: str
    score: float
    title: str
    metadata: Optional[Dict] = None

class SearchResponse(BaseModel):
    records: List[SearchResult]

class QueryParams(BaseModel):
    knowledge_id: str
    query: str
    top_k: int
    score_threshold: float

# FastAPI 应用
app = FastAPI()

def validate_auth_header(authorization: str) -> None:
    """验证 Authorization 头"""
    if not authorization:
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": ErrorCode.INVALID_AUTH,
                "error_msg": ErrorMessage.MISSING_AUTH
            }
        )
    
    auth_scheme, _, api_key = authorization.partition(' ')
    if auth_scheme.lower() != "bearer":
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": ErrorCode.INVALID_AUTH,
                "error_msg": ErrorMessage.INVALID_AUTH_FORMAT
            }
        )
    
    if api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": ErrorCode.AUTH_FAILED,
                "error_msg": ErrorMessage.AUTH_FAILED
            }
        )

def is_knowledge_exists(knowledge_id: str) -> bool:
    """检查知识库是否存在"""
    # TODO: 实现知识库验证逻辑
    return True

def validate_knowledge(knowledge_id: str) -> None:
    """验证知识库是否存在"""
    if not is_knowledge_exists(knowledge_id):
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": ErrorCode.KNOWLEDGE_NOT_FOUND,
                "error_msg": ErrorMessage.KNOWLEDGE_NOT_FOUND
            }
        )

def perform_search(query: str, retrieval_setting: RetrievalSetting) -> List[SearchResult]:
    """执行搜索操作"""
    # TODO: 实现实际的搜索逻辑
    return [
        SearchResult(
            content="Dify 是一个强大的 GenAI 应用开发平台",
            score=0.95,
            title="Dify 简介",
            metadata={
                "path": "docs/intro.txt",
                "description": "Dify 介绍文档"
            }
        )
    ]

@app.api_route("/retrieval", methods=["GET", "POST"], response_model=SearchResponse)
async def knowledge_retrieval(
    request: Request,
    authorization: str = Header(None),
    # GET参数
    knowledge_id: str = None,
    query: str = None,
    top_k: int = None,
    score_threshold: float = None,
    # POST参数
    data: InputData = None
) -> SearchResponse:
    """处理知识库检索请求"""
    # 验证认证信息
    validate_auth_header(authorization)
    
    if request.method == "GET":
        # 处理GET请求
        retrieval_setting = RetrievalSetting(
            top_k=top_k,
            score_threshold=score_threshold
        )
        # 验证知识库
        validate_knowledge(knowledge_id)
        # 执行搜索
        search_results = perform_search(query, retrieval_setting)
    else:
        # 处理POST请求
        validate_knowledge(data.knowledge_id)
        search_results = perform_search(data.query, data.retrieval_setting)
    
    return SearchResponse(records=search_results)

# uvicorn knowledge_server:app --reload

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)