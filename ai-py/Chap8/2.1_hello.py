class DatabaseConnectionError(Exception):
    """数据库连接异常类。"""
    def __init__(self, message="数据库连接失败"):
        super().__init__(message)
    
    def __str__(self):
        return f"数据库连接错误: {self.args[0]}"

def connect_to_database(db_url: str) -> bool:
    """
    连接到数据库
    
    Args:
        db_url: 数据库连接URL，必须以'db://'开头
        
    Returns:
        bool: 连接成功返回True
        
    Raises:
        DatabaseConnectionError: 当URL格式不正确时抛出
    """
    if not isinstance(db_url, str):
        raise TypeError("数据库URL必须是字符串类型")
        
    if not db_url.startswith('db://'):
        raise DatabaseConnectionError('数据库URL必须以db://开头')
        
    print(f'正在连接到数据库: {db_url}')
    return True