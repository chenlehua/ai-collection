import matplotlib.pyplot as plt
import torch
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)
y = -3 * x + 4 + np.random.randint(-2, 2, size=100)
# plt.scatter(x, y)


# 需要计算得到的参数
w = torch.ones(1, requires_grad=True)
b = torch.ones(1, requires_grad=True)

# 数据
x_tensor = torch.from_numpy(x)
y_tensor = torch.from_numpy(y)


def mse(label, pred):
    diff = label - pred
    return torch.sqrt((diff ** 2).mean())


pred = x_tensor * w + b
loss = mse(y_tensor, pred)
print(loss)  # 误差

for _ in range(20):
    # 重新定义一下，梯度清空
    w = w.clone().detach().requires_grad_(True)
    b = b.clone().detach().requires_grad_(True)

    # 正向传播
    pred = x_tensor * w + b
    loss = mse(y_tensor, pred)
    print(loss)

    loss.backward()
    w = w - w.grad * 0.05
    b = b - b.grad * 0.05

    # 正向传播、计算损失、计算梯度、参数更新
    # 多步的训练，随机梯度下降

pred = x_tensor * w + b
plt.scatter(x, y)
plt.plot(x, pred.data.numpy())
plt.legend(['y=-3x+4', 'Network'])
plt.show()