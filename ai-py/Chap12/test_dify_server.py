import pytest
from fastapi.testclient import TestClient
from dify_server import app

client = TestClient(app)

# 测试数据
VALID_API_KEY = "123456"
INVALID_API_KEY = "wrong_key"

def test_ping_endpoint_with_valid_auth():
    """测试 ping 端点 - 使用有效认证"""
    response = client.post(
        "/api/dify/receive",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"},
        json={"point": "ping"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": "pong"}

def test_unauthorized_access():
    """测试未授权访问"""
    response = client.post(
        "/api/dify/receive",
        headers={"Authorization": f"Bearer {INVALID_API_KEY}"},
        json={"point": "ping"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

def test_weather_query_valid_city():
    """测试天气查询 - 有效城市"""
    response = client.post(
        "/api/dify/receive",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"},
        json={
            "point": "app.external_data_tool.query",
            "params": {
                "app_id": "test-app-id",
                "tool_variable": "weather_data",
                "inputs": {"location": "珠海"},
                "query": "查询天气"
            }
        }
    )
    assert response.status_code == 200
    assert "城市: 珠海" in response.json()["result"]
    assert "温度" in response.json()["result"]

def test_weather_query_invalid_city():
    """测试天气查询 - 无效城市"""
    response = client.post(
        "/api/dify/receive",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"},
        json={
            "point": "app.external_data_tool.query",
            "params": {
                "app_id": "test-app-id",
                "tool_variable": "weather_data",
                "inputs": {"location": "不存在的城市"},
                "query": "查询天气"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["result"] == "未知城市"

def test_invalid_endpoint():
    """测试无效的端点"""
    response = client.post(
        "/api/dify/receive",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"},
        json={"point": "invalid_endpoint"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not implemented" 


# pip install pytest httpx
# pytest test_dify_server.py -v