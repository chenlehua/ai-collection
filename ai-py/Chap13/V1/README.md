Chap11/
├── src/
│   └── knowledge_server.py     # 现有的服务器代码
├── Dockerfile                  # Docker构建文件
├── docker-compose.yml         # Docker Compose配置
├── requirements.txt          # Python依赖
├── .dockerignore            # Docker忽略文件
└── README.md               # 项目说明文档


两种构建方法
# 在 Chap11 目录下运行
docker-compose build


# 在 Chap11 目录下运行
docker build -t knowledge-server .


# 运行
docker-compose up -d


# 测试
curl "http://localhost:8000/retrieval?knowledge_id=xxx&query=xxx&top_k=5&score_threshold=0.8" \
-H "Authorization: Bearer 123456"