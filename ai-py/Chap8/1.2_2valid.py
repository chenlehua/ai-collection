class Calculator:
    @validate_inputs(lambda x, y: isinstance(x, (int, float)) and isinstance(y, (int, float)))
    @handle_errors(default_value=0)
    def add(self, x, y):
        return x + y

    @validate_inputs(lambda x, y: isinstance(x, (int, float)) and isinstance(y, (int, float)) and y != 0)
    @handle_errors(default_value=float('inf'))
    def divide(self, x, y):
        return x / y

# 测试代码
calc = Calculator()

# 正常操作
print(calc.add(10, 5))  # 输出: 15
print(calc.divide(10, 2))  # 输出: 5.0

# 输入验证失败
try:
    print(calc.add(10, "5"))  # 触发输入验证错误
except ValueError as e:
    print(e)  # 输出: Input validation failed for add

# 错误处理
print(calc.divide(10, 0))  # 输出: Error in divide: division by zero \n inf