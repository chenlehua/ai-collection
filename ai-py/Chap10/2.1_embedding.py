from sentence_transformers import SentenceTransformer
import numpy as np
from dashscope import TextEmbedding

def cosine_similarity(a, b):
    """计算两个向量之间的余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 加载中文预训练模型
st_model = SentenceTransformer('moka-ai/m3e-base')
ds_model = TextEmbedding()

# 示例文档集合
documents = [
    "深度学习是人工智能的一个重要分支",
    "机器学习通过数据来训练模型",
    "自然语言处理让计算机理解人类语言",
    "今天天气真不错，适合出去散步",
]

# 用户查询
query = "什么是人工智能技术？"

# 使用SentenceTransformer生成文档和查询的向量表示
st_doc_embeddings = st_model.encode(documents)
st_query_embedding = st_model.encode(query)

# 使用DashScope生成文档和查询的向量表示
ds_doc_embeddings = [TextEmbedding.call(input=doc, model=TextEmbedding.Models.text_embedding_v2)['output']['embeddings'][0]['embedding'] for doc in documents]
ds_query_embedding = TextEmbedding.call(input=query, model=TextEmbedding.Models.text_embedding_v2)['output']['embeddings'][0]['embedding']

# 计算查询与每个文档的相似度（SentenceTransformer）
st_similarities = [
    (cosine_similarity(st_query_embedding, doc_embedding), doc)
    for doc_embedding, doc in zip(st_doc_embeddings, documents)
]

# 计算查询与每个文档的相似度（DashScope）
ds_similarities = [
    (cosine_similarity(ds_query_embedding, doc_embedding), doc)
    for doc_embedding, doc in zip(ds_doc_embeddings, documents)
]

# 按相似度降序排序
st_similarities.sort(reverse=True)
ds_similarities.sort(reverse=True)

# 打印结果
print(f"查询: {query}\n")
print("SentenceTransformer相关文档排序结果:")
for score, doc in st_similarities:
    print(f"相似度: {score:.4f} - 文档: {doc}")

print("\nDashScope相关文档排序结果:")
for score, doc in ds_similarities:
    print(f"相似度: {score:.4f} - 文档: {doc}")
