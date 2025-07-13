import pandas as pd
import numpy as np

# 配置参数
USER_COUNT = 1000
SEED = 42

# 1.定义类别特征及其采样概率
sex_choices = ['男', '女']
sex_probs = [0.48, 0.52]

city_choices = ['北京', '上海', '广州', '深圳', '其他']
city_probs = [0.18, 0.17, 0.15, 0.15, 0.35]

level_choices = ['高', '中', '低']
level_probs = [0.2, 0.5, 0.3]

# 2.采样类别特征
sex_sample = np.random.choice(sex_choices, USER_COUNT, p=sex_probs)
city_sample = np.random.choice(city_choices, USER_COUNT, p=city_probs)
level_sample = np.random.choice(level_choices, USER_COUNT, p=level_probs)

# 3.生成数值特征
# 年龄：正态分布，取值范围 [18, 60]
age_sample = np.clip(
    np.random.normal(loc=35, scale=8, size=USER_COUNT),
    18, 60
).astype(int)

# 最近活跃天数：指数分布，取值范围 [1, 30]
active_days_sample = np.clip(
    np.random.exponential(scale=7, size=USER_COUNT),
    1, 30
).astype(int)

# 4.合成DataFrame
user_data = pd.DataFrame({
    '性别': sex_sample,
    '所在城市': city_sample,
    '消费水平': level_sample,
    '年龄': age_sample,
    '最近活跃天数': active_days_sample
})

# 5.保存为CSV
user_data.to_csv('user_profiles.csv', index=False, encoding='utf-8-sig')
print(f"✅ 已生成 {USER_COUNT} 条用户画像数据，已保存到 'user_profiles.csv' 文件。")
