from functools import wraps

def precondition(predicate):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert predicate(*args, **kwargs), f"Precondition failed for {func.__name__}"
            return func(*args, **kwargs)
        return wrapper
    return decorator

def postcondition(predicate):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert predicate(result), f"Postcondition failed for {func.__name__}"
            return result
        return wrapper
    return decorator

# 示例类
class Account:
    def __init__(self, balance):
        self.balance = balance

    @precondition(lambda self, amount: amount > 0)
    @postcondition(lambda result: result is True)
    def deposit(self, amount):
        self.balance += amount
        return True

    @precondition(lambda self, amount: 0 < amount <= self.balance)
    @postcondition(lambda result: result is True)
    def withdraw(self, amount):
        self.balance -= amount
        return True

# 测试代码
account = Account(100)
account.deposit(50)  # 成功
account.withdraw(30)  # 成功

try:
    account.withdraw(150)  # 失败，前置条件不满足
except AssertionError as e:
    print(e)  # 输出: Precondition failed for withdraw