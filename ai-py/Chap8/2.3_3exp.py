def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_info = {
            'function': func.__name__,
            'args': args,
            'kwargs': kwargs,
            'exception': str(e)
        }
        suggestion = get_fix_suggestion(error_info)
        print("Exception occurred:")
        print(f"Function: {func.__name__}")
        print(f"Error: {e}")
        print("LLM建议:")
        print(suggestion)
        # 根据需要，可以选择应用修复措施
        return None

def get_fix_suggestion(error_info):
    prompt = f"""
在执行函数 {error_info['function']} 时发生异常。

参数：
args: {error_info['args']}
kwargs: {error_info['kwargs']}

异常信息：
{error_info['exception']}

请分析可能的原因，并提供修复建议。
"""
    suggestion = call_llm(prompt)
    return suggestion

def call_llm(prompt):
    # 调用实际的LLM接口
    # 简化为示例建议
    return "可能原因：传入的参数类型不正确。建议检查函数调用时的参数，确保与函数定义匹配。"

# 使用示例
def divide(a, b):
    return a / b

result = safe_execute(divide, 10, 0)  # 将引发ZeroDivisionError
