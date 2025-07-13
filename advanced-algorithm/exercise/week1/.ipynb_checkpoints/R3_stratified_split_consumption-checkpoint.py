import pandas as pd
from sklearn.model_selection import train_test_split

# 1. 读取数据
DATA_PATH = "user_profiles.csv"
df = pd.read_csv(DATA_PATH)

# 2. 统计“消费水平”在全体数据中的分布（黄金标准）
golden_dist = df["消费水平"].value_counts(normalize=True).sort_index()
print("【基准标准】全体数据的“消费水平”分布：")
for level, ratio in golden_dist.items():
    print(f"  {level:<2} : {ratio:.2%}")

# 3. 基于“消费水平”分层抽样划分训练集与测试集
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["消费水平"]
)

# 4. 训练集分布
train_dist = train_df["消费水平"].value_counts(normalize=True).sort_index()
print("\n【分层采样后-训练集】消费水平分布：")
for level, ratio in train_dist.items():
    print(f"  {level:<2} : {ratio:.2%}")

# 5. 测试集分布
test_dist = test_df["消费水平"].value_counts(normalize=True).sort_index()
print("\n【分层采样后-测试集】消费水平分布：")
for level, ratio in test_dist.items():
    print(f"  {level:<2} : {ratio:.2%}")

# 【可选】合并展示
print("\n【对比总结】")
summary = pd.DataFrame({
    '全体数据': golden_dist,
    '训练集': train_dist,
    '测试集': test_dist
})
print(summary.apply(lambda col: col.map(lambda x: f"{x:.2%}")))
