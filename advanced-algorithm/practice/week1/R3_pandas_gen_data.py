import pandas as pd
import numpy as np

# 定义姓名选项
names = ['小王', '李华']

# 生成10行随机数据

data = {
    '姓名': np.random.choice(names, 10),
    '年龄': np.random.randint(18, 61, 10),
    '性别': np.random.choice(['男', '女'], 10)
}

# 创建DataFrame
df = pd.DataFrame(data)
print(df)
