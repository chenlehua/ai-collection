# BGE-m3文本嵌入 + 逻辑回归情感分类
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
# 只保留必要的导入
import matplotlib.pyplot as plt
# seaborn已删除，只使用matplotlib进行可视化
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 创建示例情感数据集 ---
print("创建示例情感数据集...")

sample_data = {
    '文本': [
        # 正面情感 (label=1)
        "这个产品真的太棒了，我非常满意！",
        "服务态度很好，工作人员很热情",
        "质量超出了我的预期，强烈推荐",
        "今天心情特别好，阳光明媚",
        "这家餐厅的菜品味道很赞",
        "同事们都很友善，工作环境很棒",
        "这次旅行非常愉快，风景如画",
        "孩子们玩得很开心，活动组织得很好",
        "学到了很多新知识，收获满满",
        "朋友的生日聚会办得很成功",
        "非常感谢大家的帮助和支持",
        "这次合作非常成功，期待下次",
        "团队协作效果很好，目标达成了",
        "新功能使用起来很方便",
        "客户反馈非常积极正面",

        # 负面情感 (label=0)
        "这个产品质量太差了，完全不值这个价钱",
        "服务态度恶劣，让人很不舒服",
        "等了很久都没有得到回复，很失望",
        "今天遇到了很多麻烦事，心情糟糕",
        "这家店的食物难吃，环境也不好",
        "工作压力太大，每天都很疲惫",
        "天气太热了，让人烦躁不安",
        "交通堵塞严重，浪费了很多时间",
        "考试成绩不理想，感到很沮丧",
        "设备出现故障，影响了正常工作",
        "系统响应速度太慢，需要优化",
        "这个错误一直解决不了，很头疼",
        "预算不足，项目可能要延期",
        "沟通效率很低，浪费时间",
        "技术方案存在严重缺陷"
    ],
    'label': [
        # 正面=1 (15个)
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        # 负面=0 (15个)
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
}

df = pd.DataFrame(sample_data)
print(f"数据集大小: {len(df)}")
print(f"标签分布:\n{df['label'].value_counts()}")
print("标签含义: 0=负面, 1=正面")

# --- 2. 加载BGE-m3模型并提取特征 ---
print("\n加载BGE-m3模型...")
MODEL_NAME = "BAAI/bge-m3"
model = SentenceTransformer(MODEL_NAME)

print("提取文本嵌入特征...")
text_embeddings = model.encode(df['文本'].tolist(), show_progress_bar=True)
print(f"嵌入特征形状: {text_embeddings.shape}")

# --- 3. 直接训练逻辑回归模型 ---
print("\n训练二分类逻辑回归模型...")

X = text_embeddings
y = df['label']

# 直接用所有数据训练，使用默认参数
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X, y)

print("训练完成！")

# --- 4. 权重分析 ---
print("\n=== 权重分析 ===")

# 获取逻辑回归的权重矩阵
coefficients = model.coef_
print(f"权重矩阵形状: {coefficients.shape}")
print(f"特征维度数: {coefficients.shape[1]}")
print(f"类别数: {coefficients.shape[0]}")

# 计算每个维度的重要性（权重绝对值）
feature_importance = np.abs(coefficients[0])
print(f"特征维度数: {coefficients.shape[1]}")
print(f"最重要维度重要性: {np.max(feature_importance):.3f}")

# 找出Top 10权重贡献最大的维度（按绝对值排序）
top_10_indices = np.argsort(feature_importance)[-10:]
print(f"\nTop 10 权重贡献维度（按绝对值排序）:")
for i, idx in enumerate(reversed(top_10_indices)):
    actual_weight = coefficients[0][idx]
    print(f"  维度 {idx}: {actual_weight:.3f}")

# 可视化Top 10重要维度的LR权重
top_10_indices = np.argsort(feature_importance)[-10:]

plt.figure(figsize=(12, 8))
weights_top10 = coefficients[0][top_10_indices]  # 二分类只有一个权重向量

# 统一颜色显示权重
plt.bar(range(len(top_10_indices)), weights_top10, color='steelblue', alpha=0.7)

plt.xlabel('Top 10 重要维度')
plt.ylabel('LR权重值')
plt.title('Top 10重要维度的LR权重分布')
plt.xticks(range(len(top_10_indices)), [f'维度{idx}' for idx in top_10_indices])
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n🎨 权重可视化完成！")
print("✅ 二分类情感分析（正面 vs 负面）训练完成")