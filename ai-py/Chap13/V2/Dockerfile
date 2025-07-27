FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && pip install prometheus-fastapi-instrumentator prometheus-client

# 创建src目录并复制文件
COPY src/ /app/src/

# 设置Python路径
ENV PYTHONPATH=/app

CMD ["uvicorn", "src.knowledge_server:app", "--host", "0.0.0.0", "--port", "8000"]