import torch

x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32, requires_grad=True)
print(x)

y = x + 2
print(y)
print(y.grad_fn)  # y就多了一个AddBackward

z = y * y * 3
out = z.mean()

print(z)  # z多了MulBackward
print(out)  # out多了MeanBackward

out.backward()

print(x.grad)
