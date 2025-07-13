from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

data = load_iris()
model = LogisticRegression()
model.fit(data.data, data.target)

print(data.feature_names)
print(data.target_names)

# 在模型训练完成后，LogisticRegression 模型的实例会有一个 coef_ 属性，它存储了模型学习到的特征系数（coefficients）。
# LogisticRegression 默认的 multi_class 模型会优化一个多项式损失函数。
# coef_ 中的每一行对应于一个类别的特征权重，它代表了该类别相对于所有其他类别的相对“支持度”。
print(model.coef_)

# 多分类逻辑回归就是：对每个类别都算一遍“得分”，通过 softmax 得到各类概率，然后选概率最大的。
x = data.data[0].reshape(1, -1)  # 将数据转换为二维数组
print(data.data[0])
# print(model.predict_proba(x))
# print(model.predict(x))
# print(data.target[0])
