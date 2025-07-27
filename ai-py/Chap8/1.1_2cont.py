class Invariant:
    def __init__(self, predicate):
        self.predicate = predicate

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.predicate(), "Invariant condition failed"

# 示例类
class Account:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def check_invariant(self):
        return self.balance >= 0

# 测试代码
account = Account(100)
with Invariant(account.check_invariant):
    account.deposit(50)
    account.withdraw(30)

try:
    with Invariant(account.check_invariant):
        account.withdraw(150)  # 失败，不变量不满足
except AssertionError as e:
    print(e)  # 输出: Invariant condition failed