from llama_index.llms.dashscope import DashScope
from llama_index.core.base.llms.types import MessageRole, ChatMessage

def invoke(user_message, stream=False):
    llm = DashScope(model="qwen-plus")
    messages = [
    ChatMessage(role=MessageRole.SYSTEM, content="你是智能助理贾维斯，用中文回答我的全部问题。"),
    ChatMessage(role=MessageRole.USER, content=user_message)
    ]
    stream_result = ""
    if stream:
        responses = llm.stream_chat(messages)
        for response in responses:
            print(response.delta, end="")
            stream_result += response.delta
        return stream_result
    else:
        return llm.chat(messages).message.content

if __name__ == "__main__":
    print(invoke("写个100字的故事", stream=True))