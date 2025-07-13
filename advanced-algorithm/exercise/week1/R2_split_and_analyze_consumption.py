import pandas as pd
from sklearn.model_selection import train_test_split

# 1. 读取数据
DATA_PATH = "user_profiles.csv"
df = pd.read_csv(DATA_PATH)

# 2. 显示全体数据的“消费水平”分布（黄金标准）
golden_dist = df["消费水平"].value_counts(normalize=True).sort_index()
print("【基准标准】全体数据的“消费水平”分布：")
for level, ratio in golden_dist.items():
    print(f"  {level}: {ratio:.2%}")

# 3. 随机划分训练集和测试集
train_df, test_df = train_test_split(
    df, test_size=0.2, random_state=42, shuffle=True
)

# 4. 统计训练集分布
train_dist = train_df["消费水平"].value_counts(normalize=True).sort_index()
print("\n【训练集】消费水平分布：")
for level, ratio in train_dist.items():
    print(f"  {level}: {ratio:.2%}")

# 5. 统计测试集分布
test_dist = test_df["消费水平"].value_counts(normalize=True).sort_index()
print("\n【测试集】消费水平分布：")
for level, ratio in test_dist.items():
    print(f"  {level}: {ratio:.2%}")

# 可选：输出结果到csv便于分析
summary_df = pd.DataFrame({
    "全体分布": golden_dist,
    "训练集": train_dist,
    "测试集": test_dist
})
summary_df.to_csv("level_dist_summary.csv", encoding="utf-8-sig")
