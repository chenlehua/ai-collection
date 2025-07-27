import pandas as pd
from datetime import datetime, timedelta

# 假设我们有一个包含日期时间的 CSV 文件
# 日期格式为 'YYYY-MM-DD HH:MM:SS'
data = {
    'event_id': [1, 2, 3, 4],
    'event_time': ['2024-11-12 14:30:00', '2024-11-12 15:45:00', '2024-11-13 09:00:00', '2024-11-14 18:15:00'],
    'event_duration_minutes': [30, 45, 60, 90]
}

# 将数据加载到 pandas DataFrame 中
df = pd.DataFrame(data)

# 将 event_time 列转换为 datetime 对象
df['event_time'] = pd.to_datetime(df['event_time'], format='%Y-%m-%d %H:%M:%S')

# 计算事件结束时间（event_end_time），基于 event_duration_minutes
df['event_end_time'] = df['event_time'] + pd.to_timedelta(df['event_duration_minutes'], unit='m')

# 计算当前时间与事件时间的差异
current_time = pd.Timestamp.now()
df['time_until_event'] = df['event_time'] - current_time

# 过滤出未来的事件
future_events = df[df['event_time'] > current_time]

# 输出处理后的数据
print(future_events)

# 处理时区信息（假设事件时间是 UTC 时间）
df['event_time_utc'] = df['event_time'].dt.tz_localize('UTC')

# 转换为本地时区（假设为 Asia/Shanghai）
df['event_time_local'] = df['event_time_utc'].dt.tz_convert('Asia/Shanghai')

# 输出带有时区转换的 DataFrame
print(df[['event_id', 'event_time_utc', 'event_time_local']])
