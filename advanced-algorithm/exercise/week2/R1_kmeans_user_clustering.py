# K-means用户画像聚类分析与代表性样本识别
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 配置与数据读取 ---
DATA_FILE = "../week1/user_profiles.csv"
MODEL_NAME = "BAAI/bge-m3"
CAT_COLS = ["性别", "所在城市", "消费水平"]
NUM_COLS = ["年龄", "最近活跃天数"]
N_CLUSTERS_RANGE = range(2, 11)

# 不再需要设置matplotlib字体，只使用plotly交互式可视化

print("正在读取用户画像数据...")
df = pd.read_csv(DATA_FILE)
print(f"数据形状: {df.shape}")
print(f"数据预览:\n{df.head()}")

# --- 2. 特征编码与标准化 ---
print("\n加载 BGE-m3 嵌入模型...")
model = SentenceTransformer(MODEL_NAME)

print("对类别特征进行编码...")
cat_vectors = []
for col in CAT_COLS:
    print(f"  编码 {col}...")
    vectors = model.encode(df[col].astype(str).tolist())
    cat_vectors.append(vectors)

# 合并所有特征
num_vectors = df[NUM_COLS].values
user_matrix = np.hstack(cat_vectors + [num_vectors])
print(f"特征拼接后形状: {user_matrix.shape}")

# 标准化
scaler = StandardScaler()
user_matrix_std = scaler.fit_transform(user_matrix)

# --- 3. 直接使用6类进行聚类 ---
optimal_k = 6
print(f"\n直接使用 k={optimal_k} 进行聚类...")

# --- 4. 使用6类进行聚类 ---
final_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = final_kmeans.fit_predict(user_matrix_std)
centroids = final_kmeans.cluster_centers_

# 添加聚类标签到数据框
df_clustered = df.copy()
df_clustered['聚类标签'] = cluster_labels

print("各聚类的用户数量:")
cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
for cluster_id, count in cluster_counts.items():
    print(f"  聚类 {cluster_id}: {count} 用户")

# --- 6. PCA降维用于可视化 ---
print("\n进行PCA降维...")
pca = PCA(n_components=3)
user_3d = pca.fit_transform(user_matrix_std)
centroids_3d = pca.transform(centroids)

exp_var = pca.explained_variance_ratio_
print(f"PCA前3个主成分解释的方差比例: {exp_var}")
print(f"累计解释方差: {np.sum(exp_var):.2%}")

# --- 7. 交互式3D可视化 ---
print("\n生成交互式3D聚类可视化...")
df_plot = df_clustered.copy()
df_plot['PC1'] = user_3d[:, 0]
df_plot['PC2'] = user_3d[:, 1]
df_plot['PC3'] = user_3d[:, 2]

# 用户点
fig3d = px.scatter_3d(
    df_plot, x='PC1', y='PC2', z='PC3',
    color='聚类标签',
    hover_data=CAT_COLS + NUM_COLS,
    title='K-means聚类结果交互式可视化',
    color_discrete_sequence=px.colors.qualitative.Set1
)

# 添加聚类中心点
centroids_df = pd.DataFrame({
    'PC1': centroids_3d[:, 0],
    'PC2': centroids_3d[:, 1],
    'PC3': centroids_3d[:, 2],
    '聚类中心': [f'中心{i}' for i in range(optimal_k)]
})

fig3d.add_trace(go.Scatter3d(
    x=centroids_df['PC1'],
    y=centroids_df['PC2'],
    z=centroids_df['PC3'],
    mode='markers+text',
    marker=dict(size=15, color='red', symbol='x'),
    text=centroids_df['聚类中心'],
    textposition='top center',
    name='聚类中心',
    showlegend=True
))

fig3d.show()

print("\n🎯 交互式3D可视化已生成！")
print("   • 可以旋转、缩放、点击查看详细信息")
print("   • 红色X标记为各聚类中心点")
print("   • 不同颜色代表不同聚类")

# --- 8. 保存结果 ---
# 保存聚类结果
df_clustered.to_csv('user_clustering_results.csv', index=False)
print(f"\n📁 聚类结果已保存到 user_clustering_results.csv")

# 计算最终聚类的轮廓系数
final_silhouette_score = silhouette_score(user_matrix_std, cluster_labels)

print(f"\n=== ✅ K-means聚类分析完成 ===")
print(f"📊 聚类数量: {optimal_k}")
print(f"🎯 轮廓系数: {final_silhouette_score:.3f}")
print(f"📈 PCA累计解释方差: {np.sum(exp_var):.2%}")
print(f"🌐 交互式可视化: 请查看浏览器中的3D图表")