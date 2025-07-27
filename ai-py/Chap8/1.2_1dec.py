from functools import wraps

def validate_inputs(validation_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validation_func(*args, **kwargs):
                raise ValueError(f"Input validation failed for {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def handle_errors(default_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                return default_value
        return wrapper
    return decorator


####

def file_operation_handler(default_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"文件未找到: {e}")
                return default_value
            except PermissionError as e:
                print(f"权限不足，无法访问文件: {e}")
                return default_value
            except IsADirectoryError as e:
                print(f"目标是一个目录，不是文件: {e}")
                return default_value
            except OSError as e:
                print(f"操作系统错误: {e}")
                return default_value
            except Exception as e:
                print(f"未预期的错误: {e}")
                return default_value
        return wrapper
    return decorator

# 使用示例
@file_operation_handler(default_value='')
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()