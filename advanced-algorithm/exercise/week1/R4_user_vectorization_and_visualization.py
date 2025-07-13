import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import plotly.express as px
from sentence_transformers import SentenceTransformer
import random

# --- 1. 配置与数据读取 ---
DATA_FILE = "user_profiles.csv"
MODEL_NAME = "BAAI/bge-m3"
CAT_COLS = ["性别", "所在城市", "消费水平"]
NUM_COLS = ["年龄", "最近活跃天数"]
COLOR_COL = "消费水平"

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv(DATA_FILE)

# --- 2. 特征编码 ---
print("加载 BGE-m3 嵌入模型...")
model = SentenceTransformer(MODEL_NAME)
print("对类别特征编码...")
cat_vectors = [
    model.encode(df[col].astype(str).tolist())
    for col in CAT_COLS
]

num_vectors = df[NUM_COLS].values
user_matrix = np.hstack(cat_vectors + [num_vectors])
print(f"特征拼接后shape: {user_matrix.shape}")

scaler = StandardScaler().fit(user_matrix)
user_matrix_std = scaler.transform(user_matrix)
print(user_matrix_std.shape)

# --- 3. PCA三维降维 ---
pca = PCA(n_components=3)
user_3d = pca.fit_transform(user_matrix_std)
exp_var_3d = pca.explained_variance_ratio_
print(f"\n--- PCA降至3维 ---")
for i, var in enumerate(exp_var_3d, 1):
    print(f"主成分{i}解释的方差：{var:.2%}")

print(f"累计解释的方差：{np.sum(exp_var_3d):.2%}")


# --- 4. 3D静态可视化（Matplotlib） ---
def plot_3d_matplotlib(X_3d, df, exp_var, color_col, n_label=20):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    color_map = {
        k: c for k, c in zip(sorted(df[color_col].unique()), plt.cm.tab10.colors)
    }
    colors = df[color_col].map(color_map)
    ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], c=colors, alpha=0.5, s=40)

    # 随机点标签
    idxs = random.sample(range(len(df)), min(n_label, len(df)))
    for i in idxs:
        label = "-".join(str(df.loc[i, col]) for col in CAT_COLS + NUM_COLS)
        ax.text(X_3d[i, 0], X_3d[i, 1], X_3d[i, 2], label, size=8)

    ax.set_xlabel(f"PC1 ({exp_var[0]:.2%})")
    ax.set_ylabel(f"PC2 ({exp_var[1]:.2%})")
    ax.set_zlabel(f"PC3 ({exp_var[2]:.2%})")
    plt.title("用户画像三维可视化 (Matplotlib)")
    plt.show()


plot_3d_matplotlib(user_3d, df, exp_var_3d, COLOR_COL, n_label=20)

# --- 5. 3D交互可视化（Plotly） ---
df_plot = df.copy()
df_plot["PC1"] = user_3d[:, 0]
df_plot["PC2"] = user_3d[:, 1]
df_plot["PC3"] = user_3d[:, 2]
fig3d = px.scatter_3d(
    df_plot,
    x="PC1", y="PC2", z="PC3",
    color=COLOR_COL,
    hover_data={col: True for col in CAT_COLS + NUM_COLS},
    title="用户画像三维可视化"
)

fig3d.update_traces(marker=dict(size=6, opacity=0.7))
fig3d.show()
