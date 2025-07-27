from llama_index.llms.dashscope import DashScope
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
import os
from duckduckgo_search import DDGS
# 安装软件包 pip install duckduckgo-search

# 设置代理
os.environ["http_proxy"] = "http://127.0.0.1:4780"
os.environ["https_proxy"] = "http://127.0.0.1:4780"

from llama_index.core import Settings
llm = DashScope(model="qwen-plus")
# 配置全局语言模型
Settings.llm = llm

# 定义搜索工具 DuckDuckGo 搜索
def search(query:str) -> str:
    """
    Args:
        query: 用户提示
    return:
        context (str): 用户查询的搜索结果
    """
    req = DDGS()
    response = req.text(query, max_results=4)
    context = ""
    for result in response:
        context += result['body']
    return context

# 用于将普通的 Python 函数转换成 AI 可以调用的工具
search_tool = FunctionTool.from_defaults(fn=search)

# 创建一个 ReActAgent 实例
agent = ReActAgent.from_tools(
    [search_tool], 
    llm=llm, 
    verbose=True,
    allow_parallel_tool_calls=True # 允许代理做出决策而无需总是依赖外部操作
)

template = """
你是一位专业的体育分析记者。
分析 阿根廷国家队 一共获得过几次世界杯冠军。
另外，在获得冠军的决赛的比赛中，将点球也计算进去的话，一共进了多少个球。
"""

responses = agent.chat(template) 
print(responses)    
