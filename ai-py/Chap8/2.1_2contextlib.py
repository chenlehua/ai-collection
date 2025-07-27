import contextlib

@contextlib.contextmanager
def file_manager(file_path, mode):
    """
    一个用于文件操作的上下文管理器。
    
    这个装饰器使用@contextlib.contextmanager将普通函数转换为上下文管理器。
    函数的执行过程:
    1. try块中打开文件
    2. yield语句将控制权交给with语句内的代码块
    3. finally块确保文件始终被关闭
    
    参数:
        file_path: 文件路径
        mode: 文件打开模式('r'读取,'w'写入等)
        
    异常:
        IOError: 当文件操作发生错误时抛出
        
    用法:
        with file_manager('data.txt', 'r') as f:
            data = f.read()
    """
    file = None
    try:
        file = open(file_path, mode)
        yield file
    except IOError as e:
        print(f"文件操作异常: {e}")
        raise
    finally:
        if file:
            file.close()

# 使用上下文管理器
with file_manager('data.txt', 'r') as f:
    data = f.read()

# 通过自定义的file_manager，可以确保文件在任何情况下都能被正确关闭，避免资源泄漏