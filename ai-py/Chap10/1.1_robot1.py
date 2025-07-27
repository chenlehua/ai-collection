from chat import rag
''' 封装RAG '''
index = rag.load_index()
query_engine = rag.create_query_engine(index)
rag.ask("100字以内，简要回答RAG的4个典型应用场景", query_engine, stream=True)
