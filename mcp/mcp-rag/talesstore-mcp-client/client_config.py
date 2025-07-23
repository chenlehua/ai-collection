from os import environ
from openai import AsyncOpenAI

# 从环境变量中读取配置信息
# 配置MCP服务器主机地址，默认为本地8080端口的SSE服务
MCP_SERVER_HOST = environ.get('MCP_SERVER_HOST', 'http://localhost:8080/sse')
# 配置LLM API的基础URL，默认使用阿里云DashScope兼容模式API
LLM_API_BASE_URL = environ.get('LLM_API_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
# 配置使用的LLM模型，默认为qwen-max
LLM_MODEL = environ.get('LLM_MODEL', 'qwen-max')
# 配置LLM API密钥
LLM_API_KEY = environ.get('LLM_API_KEY', 'sk-666814d1fbc447e4f2ab401be341a9a7598')

# 初始化异步OpenAI客户端，用于与LLM模型通信
llm_client = AsyncOpenAI(
    base_url=LLM_API_BASE_URL,
    api_key=LLM_API_KEY,
)

# 文本分析提示模板：用于将原始文本切段并生成FAQ
# 该模板指导LLM如何处理文本，包括切段规则和FAQ生成要求
analysis_content_prompt_template = '''
需要将以下文本切段，并根据文本内容整理 FAQ。
文本切段的要求是：
1. 保证语义的完整性：不要将一个完整的句子切断，不要把表达同一个语义的不同句子分割开
2. 保留足够多的上下文信息：如果切割后的文本段必须依赖上下文信息才能表达正确的语义，那就不能切割开
3. 过滤无效信息：过滤格式化内容如大量填充的空格，过滤不完整的段落以及过滤
4. 移除 markdown 内容的标记，层次关系按 1，2，3 以及 1.1，2.1 来标记
5. 只保留文本内容，移除链接等信息
6. 不要对标题单独切段：仅对正文进行切段，标题可以与正文合并一起，或者是作为上下文信息扩充进正文分段内
7. 切段后的文本如果不是一个完整的句子，请修改为一个完整表述的句子

FAQ 的要求是：
1. FAQ 的问题范围尽量小，提出比较原子的问题
2. 对主要内容整理 FAQ，FAQ 的数量不大于 20 个

直接输出整理后的结果，结果格式为：
{
    "Chunks":["<chunk_0>", "<chunk_1>"],
    "FAQs": [
    {"Question": "<question_0>", "Answer": "<answer_0>"},
    {"Question": "<question_0>", "Answer": "<answer_0>"}
    ]
}

文本内容:
%s

'''

# FAQ存储提示模板：用于将问题和答案存储到FAQ库中
# 格式化问答对，以便存入知识库系统
store_faq_prompt_template = '''
将以下内容存储入 FAQ 库内：
Question：%s
Answer：%s
'''

# 知识存储提示模板：用于将文本内容存储到Knowledge知识库中
store_knowledge_prompt_template = '''
将以下内容存储入 Knowledge 知识库内：
%s
'''

# 搜索提示模板：指导LLM如何检索知识库和FAQ库并返回相关内容
# 该模板定义了检索的步骤和返回结果的格式
search_prompt_template = '''
你是产品答疑助手，在回答问题之前请先检索 Knowledge 库和 FAQ 库：
1. 先理解问题并对问题进行拆解，拆解成多个子问题。
2. 每个子问题同时检索 Knowledge 库和 FAQ 库，每次检索结果不超过 20 条
3. 对检索的内容进行筛选，保留与问题最相关的内容，Knowledge 和 FAQ 分别不超过 10 条。

最后合并检索内容，返回与检索内容最相关的 20 条，直接返回检索的结果，样例如下：
1. 如果是 Knowledge，格式为：Knowledge：<结果一>
2. 如果是 FAQ，格式为：FAQ：<结果二>

检索内容：
%s
'''

# 聊天提示模板：用于引导LLM如何基于检索到的知识回答用户问题
# 定义了问题拆解、检索和回答的流程
chat_prompt_template = '''
你是产品答疑助手，在回答问题之前请先检索 Knowledge 库和 FAQ 库：
1. 先理解问题并对问题进行拆解，拆解成多个子问题，子问题尽量是比较小比较原子的问题。
2. 每个子问题同时检索 Knowledge 库和 FAQ 库，每次检索结果不超过 10 条，最后合并所有子问题的检索结果。

对检索的内容进行筛选，保留与问题最相关的检索结果，利用检索到的内容进行回答，不要乱给答案。

我的问题是：
%s
'''