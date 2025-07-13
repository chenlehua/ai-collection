from sklearn.model_selection import train_test_split

# K折交叉验证
from sklearn.model_selection import KFold
from sklearn.model_selection import RepeatedKFold

# K折分布保持交叉验证
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold

# 时间序列划分方法
from sklearn.model_selection import TimeSeriesSplit

# bootstrap采样，上采样，下采样
from sklearn.utils import resample

# 生成模拟的数据和标签
import numpy as np

X = np.zeros((20, 5))
Y = np.array([1] * 5 + [2] * 5 + [3] * 5 + [4] * 5)
print(X, Y)

# 直接按照比例拆分
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2)
print(f"train_X:{train_X}")
print(f"test_X:{test_X}")
print(f"train_Y:{train_Y}")
print(f"test_Y:{test_Y}")

# 按照比例 & 标签分布划分
train_X, test_X, train_y, test_Y = train_test_split(X, Y, test_size=0.2, stratify=Y)
print(f"train_X:{train_X}")
print(f"test_X:{test_X}")
print(f"train_Y:{train_Y}")
print(f"test_Y:{test_Y}")

# 交叉验证划分
kf = KFold(n_splits=5)
for train_idx, test_idx in kf.split(X, Y):
    print(f"train_idx:{train_idx}, test_idx:{test_idx}, feature:{X[train_idx]}, Label:{Y[test_idx]}")
