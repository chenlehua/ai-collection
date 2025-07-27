import pandas as pd
import numpy as np

# 设置随机种子以确保结果可重复
np.random.seed(42)

# 定义数据集的大小
num_rows = 10_000_000  # 1000万行数据

# 定义类别和区域的选项
categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Books', 'Sports']
regions = ['North', 'South', 'East', 'West']

# 生成随机数据
data = {
    'category': np.random.choice(categories, size=num_rows),
    'region': np.random.choice(regions, size=num_rows),
    'sales': np.random.uniform(10, 1000, size=num_rows)  # 销售额在 10 到 1000 之间
}

# 创建 DataFrame
df = pd.DataFrame(data)

# 将 DataFrame 保存为 CSV 文件
df.to_csv('large_dataset.csv', index=False)

print("large_dataset.csv 文件已生成，包含 1000 万行数据。")
