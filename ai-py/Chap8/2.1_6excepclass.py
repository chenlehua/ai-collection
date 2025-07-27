def process_data(data):
    try:
        # 数据处理逻辑
        result = data['key'] * 10
    except KeyError as e:
        print(f"缺少关键字段: {e}")
        raise DataValidationError("数据验证失败", data)
    except TypeError as e:
        print(f"数据类型错误: {e}")
        raise DataValidationError("数据类型不匹配", data)

# 自定义异常类
class DataValidationError(Exception):
    """数据验证失败异常。"""

    def __init__(self, message, data):
        super().__init__(message)
        self.data = data
        print(f"产生异常的变量: {self.data}")

d = 'string'
process_data(d)