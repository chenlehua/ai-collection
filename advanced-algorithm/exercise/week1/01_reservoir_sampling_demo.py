# 目标：体验如何从大数据流/大文件中等概率采样k个样本
# 场景：适用于数据太大，无法整体加载入内存时的高效采样


import csv
import random


def reservoir_sampling(file_path, k=10):
    """
    从大文件或数据流中等概率采样k个样本。
    :param file_path: 输入文件路径（CSV格式，含表头）
    :param k: 采样数量
    :return: 采样到的样本（字典列表）
    """
    reservoir = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < k:
                reservoir.append(row)
            else:
                j = random.randint(0, i)
                if j < k:
                    reservoir[j] = row
    return reservoir


if __name__ == "__main__":
    K = 10  # 可自定义采样数量
    FILE = "user_profiles.csv"
    print(f"开始对 {FILE} 进行蓄水池采样，目标采样数量：{K}")
    samples = reservoir_sampling(FILE, K)
    print(f"\n蓄水池采样得到的 {K} 个用户画像示例：")
    for idx, user in enumerate(samples, 1):
        user_desc = ", ".join([f"{k}:{v}" for k, v in user.items()])
        print(f"{idx:>2d}: {user_desc}")
