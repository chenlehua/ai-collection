"""
# 集成 DeepSeek 的 MCP 客户端[LangChain版]
#更详细的使用方法请参考：https://github.com/langchain-ai/langchain-mcp-adapters

# 所需环境变量：
# DEEPSEEK_API_KEY：DeepSeek API 密钥 (格式：sk-xxxx...)
# DEEPSEEK_BASE_URL：DeepSeek API 基础 URL (https://api.deepseek.com)
# DEEPSEEK_MODEL：DeepSeek 模型名称 (例如 deepseek-chat)

Author: FlyAIBox
Date: 2025.05.04
"""
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import logging

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import chat_agent_executor
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 优先从环境变量加载API密钥等信息
load_dotenv()

# 配置和风天气API环境变量（如果在环境中不存在）
if not os.getenv("QWEATHER_API_KEY"):
    os.environ["QWEATHER_API_KEY"] = "XXX"  # 请替换为实际的API密钥
if not os.getenv("QWEATHER_API_BASE"):
    os.environ["QWEATHER_API_BASE"] = "https://n83tefhk3u.re.qweatherapi.com/v7"

print(os.getenv("DEEPSEEK_API_KEY", ""))

# 配置 ChatOpenAI
model = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0
)


async def main():
    # 确定服务器路径
    server_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "server",
        "weather_server.py"
    )

    # 检查服务器文件是否存在
    if not os.path.exists(server_path):
        logger.error(f"错误: 服务器文件不存在: {server_path}")
        return

    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
    )

    try:
        logger.info("正在启动客户端连接...")
        async with stdio_client(server_params) as (read, write):
            logger.info("成功建立客户端连接")

            async with ClientSession(read, write) as session:
                # Initialize the connection
                logger.info("正在初始化会话...")
                await session.initialize()
                logger.info("会话初始化成功")

                # Get tools
                logger.info("正在加载MCP工具...")
                tools = await load_mcp_tools(session)
                logger.info(f"成功加载工具: {[tool.name for tool in tools]}")

                # 创建提示模板
                prompt = SystemMessage(content=""""                      
                                  """)

                # Create and run the agent
                logger.info("正在创建agent...")
                agent = create_react_agent(
                    model=model,
                    tools=tools,
                    prompt=prompt
                )
                logger.info("Agent创建成功")

                # 发送查询
                logger.info("正在发送天气查询...")
                agent_response = await agent.ainvoke({
                    "messages": "最近一周郑州有没有高温或大风预警？周末适合户外活动吗？"
                })

                # 打印响应
                logger.info("\nAgent Response:")
                print(agent_response)

                # 遍历消息列表并打印 ToolMessage 的 content
                if 'messages' in agent_response:
                    print("\n--- Tool Message Contents ---")
                    for message in agent_response['messages']:
                        print(f"\nTool: {message.name}")  # 可以选择打印工具名称
                        print(f"Content:\n{message.content}")
                        print("-" * 20)  # 分隔不同 ToolMessage 的内容

    except Exception as e:
        logger.error(f"运行过程中发生错误: {str(e)}", exc_info=True)
        # 如果是TaskGroup相关的错误，打印更详细的信息
        if "TaskGroup" in str(e) and hasattr(e, "__cause__"):
            logger.error(f"TaskGroup错误详情: {str(e.__cause__)}")

if __name__ == "__main__":
    asyncio.run(main())
