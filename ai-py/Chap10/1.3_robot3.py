from chat import llm
''' 提示词与意图识别 '''

# 定义角色和能力的提示信息
prompt = '''
【角色】
你是一个问题分类路由器，需要识别问题的类型。
---
【能力】
问题的类型目前有：公司内部文档查询、内容翻译
---
【限制】
你只能选择一类意图作为你的判断，并不要说任何无关内容。
---
【用户输入】
以下是用户输入，请判断：
'''

def get_question_type(question):
    """
    获取问题的类型

    参数:
    - question (str): 需要判断的问题文本

    返回值:
    - str: 问题类型，可能是“公司内部文档查询”或"内容翻译"
    """
    # 调用语言模型以获取问题类型
    return llm.invoke(prompt + question)

# 示例调用
if __name__ == "__main__":
    # print(get_question_type('who is the author of the book "The Great Gatsby"'))
    # print('\n')
    # print(get_question_type('rag有哪些优点？'))
    # print('\n')

    # question = '100字以内rag的应用场景？'
    question = '"The Great Gatsby" is a novel written by F. Scott Fitzgerald.'
    if get_question_type(question) == '公司内部文档查询':
        print('需要调用公司内部文档查询')
        import chat.rag as rag
        rag.ask(question, query_engine=rag.create_query_engine(index=rag.load_index()))
    elif get_question_type(question) == '内容翻译':
        print('需要调用内容翻译的API')
        result = llm.invoke(f'你是一名翻译专家，你要识别不同语言的文本，并翻译为中文。\n{question}')
        print(result)