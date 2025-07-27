import os
import shutil
import numpy as np
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from lightrag.llm import openai_complete_if_cache, openai_embedding

#########
# Uncomment the below two lines if running in a jupyter notebook to handle the async nature of rag.insert()
# import nest_asyncio
# nest_asyncio.apply()
#########

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WORKING_DIR = "./dickens"

# 如果目录存在，删除它及其所有内容
# if os.path.exists(WORKING_DIR):
#     shutil.rmtree(WORKING_DIR)

# 创建新的空目录
# os.mkdir(WORKING_DIR)

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    return await openai_complete_if_cache(
        "qwen-plus",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs
    )

async def embedding_func(texts: list[str]) -> np.ndarray:
    # 将文本列表分成每组25个的批次
    batch_size = 25
    batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
    
    # 对每个批次分别获取嵌入向量
    all_embeddings = []
    for batch in batches:
        batch_embeddings = await openai_embedding(
            batch,
            model="text-embedding-v2",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        all_embeddings.extend(batch_embeddings)
    
    return np.array(all_embeddings)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=1536,
        max_token_size=8192,
        func=embedding_func
    )
)

# with open("./book.txt", encoding="utf-8") as f:
#     rag.insert(f.read())

# Perform naive search
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="naive")))

# Perform local search
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="local")))

# Perform global search
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="global")))

# Perform hybrid search
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="hybrid")))