import pandas as pd
import numpy as np
from scipy import stats

# 示例数据：来自两个不同数据源的股票交易数据
data_source_1 = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'Stock': ['AAPL', 'AAPL', 'AAPL', 'AAPL'],
    'Price': [150, 152, 10000, 153],  # 10000 是异常值
    'Volume': [1000, 1100, 1200, 1300]
})

data_source_2 = pd.DataFrame({
    'Date': ['01/01/2023', '01/02/2023', '01/03/2023', '01/04/2023'],
    'Stock': ['AAPL', 'AAPL', 'AAPL', 'AAPL'],
    'Price': [149, 151, 152, np.nan],  # 最后一行缺失值
    'Volume': [1050, 1150, 1250, 1350]
})

# 1. 数据加载与初步检查
def load_and_inspect_data(data_sources):
    # 将来自不同数据源的数据合并为一个数据集
    data = pd.concat(data_sources, ignore_index=True)
    
    # 检查数据的基本信息和缺失值情况
    print("数据概览：")
    print(data.info())
    print("\n缺失值统计：")
    print(data.isnull().sum())
    
    return data

# 2. 异常值检测与处理
# 提供了两种异常值检测方法：
#     Z-score：通过计算 Z-score 来检测异常值，Z-score 超过指定阈值的点被认为是异常值。
#     IQR（四分位距）：通过计算 IQR 来检测异常值，超出 1.5 倍 IQR 范围的点被认为是异常值。
#     检测到的异常值会被替换为 NaN，以便后续处理。
def detect_and_handle_outliers(data, column, method='zscore', threshold=3):
    """
    使用 Z-score 或 IQR 方法检测并处理异常值。
    
    :param data: 输入数据
    :param column: 需要检测异常值的列
    :param method: 异常值检测方法，'zscore' 或 'iqr'
    :param threshold: 异常值检测的阈值
    :return: 处理后的数据
    """
    if method == 'zscore':
        # 使用 Z-score 检测异常值
        z_scores = np.abs(stats.zscore(data[column].dropna()))
        # 创建一个与原始数据相同长度的布尔索引
        outliers_mask = pd.Series(False, index=data.index)
        # 将非空值的位置设置为对应的异常值标记
        outliers_mask[data[column].notna()] = z_scores > threshold
        print(f"检测到 {outliers_mask.sum()} 个异常值（Z-score > {threshold}）")
        
        # 将异常值替换为 NaN
        data.loc[outliers_mask, column] = np.nan
    
    elif method == 'iqr':
        # 使用 IQR 检测异常值
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
        print(f"检测到 {outliers.sum()} 个异常值（IQR）")
        
        # 将异常值替换为 NaN
        data.loc[outliers, column] = np.nan
    
    return data

# 3. 缺失值处理
# 提供了三种缺失值处理方法：
#     均值填充：使用列的均值填充缺失值。
#     中位数填充：使用列的中位数填充缺失值。
#     删除缺失值：删除包含缺失值的行。
def handle_missing_values(data, method='mean'):
    """
    处理缺失值。
    
    :param data: 输入数据
    :param method: 缺失值处理方法，'mean'、'median' 或 'drop'
    :return: 处理后的数据
    """
    # 只选择数值类型的列
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    
    if method == 'mean':
        # 只对数值列使用均值填充缺失值
        data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
    elif method == 'median':
        # 只对数值列使用中位数填充缺失值
        data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())
    elif method == 'drop':
        # 删除包含缺失值的行
        data.dropna(inplace=True)
    
    return data

# 4. 格式统一
def unify_data_format(data):
    # 统一日期格式为 datetime 类型，确保不同来源的数据格式一致。
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    
    # 处理货币单位（假设价格是以不同货币单位表示的）
    # 这里我们假设所有价格都是以美元为单位，如果有其他货币单位，可以在这里进行转换
    # 比如：data['Price'] = data['Price'] * 汇率
    
    return data

# 5. 数据融合
# 将所有步骤整合在一起，形成一个完整的清洗流程。
# 该流程包括数据加载、格式统一、异常值处理、缺失值处理等步骤。
def merge_data_sources(data_sources):
    # 加载并检查数据
    data = load_and_inspect_data(data_sources)
    
    # 统一数据格式
    data = unify_data_format(data)
    
    # 检测并处理异常值
    data = detect_and_handle_outliers(data, 'Price', method='zscore', threshold=3)
    
    # 处理缺失值
    data = handle_missing_values(data, method='mean')
    
    return data

# 测试数据清洗流程
cleaned_data = merge_data_sources([data_source_1, data_source_2])

# 查看清洗后的数据
print("\n清洗后的数据：")
print(cleaned_data)
