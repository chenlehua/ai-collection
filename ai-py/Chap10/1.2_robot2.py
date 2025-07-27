from llama_index.core import PromptTemplate
from chat import rag
''' 提示词 '''
prompt_template = PromptTemplate(
    template="""
    你是一个叫做贾维斯的智能助理，每次在回答问题前加上"贾维斯说:"。
    参考格式如下：
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "问题：{query_str}\n。"
    "贾维斯说："
    """
)


index = rag.load_index()
query_engine = rag.create_query_engine(index)
query_engine.update_prompts({"response_synthesizer:text_qa_template": prompt_template})
rag.ask("100字以内，简要回答RAG的4个典型应用场景", query_engine, stream=True)
