import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 设置Seaborn的蓝色主题
sns.set_theme(style="whitegrid", palette="Blues")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False     # 用来正常显示负号

# 生成测试数据
np.random.seed(42)
categories = ['A', 'B', 'C', 'D']
subcategories = ['X', 'Y', 'Z']
data = pd.DataFrame({
    'Category': np.random.choice(categories, size=100),
    'Subcategory': np.random.choice(subcategories, size=100),
    'Value': np.random.randint(1, 10, size=100)
})

# 通用绘图函数
def plot_chart(data, chart_type='stacked_bar', category_col='Category', subcategory_col='Subcategory', value_col='Value'):
    """
    通用绘图函数，支持堆积柱状图和饼图。
    
    :param data: 输入数据，pandas DataFrame 格式
    :param chart_type: 图表类型，'stacked_bar' 或 'pie'
    :param category_col: 类别列的名称
    :param subcategory_col: 子类别列的名称
    :param value_col: 值列的名称
    """
    # 检查数据是否包含必要的列
    if category_col not in data.columns or value_col not in data.columns:
        raise ValueError(f"数据必须包含 '{category_col}' 和 '{value_col}' 列")

    # 生成堆积柱状图
    if chart_type == 'stacked_bar':
        if subcategory_col not in data.columns:
            raise ValueError(f"数据必须包含 '{subcategory_col}' 列用于堆积柱状图")
        
        # 透视数据，准备堆积柱状图
        pivot_data = data.pivot_table(index=category_col, columns=subcategory_col, values=value_col, aggfunc='sum', fill_value=0)
        
        # 绘制堆积柱状图
        ax = pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=sns.color_palette("Blues", len(pivot_data.columns)))
        
        # 设置标题和标签
        ax.set_title('堆积柱状图示例', fontsize=16)
        ax.set_xlabel(category_col, fontsize=12)
        ax.set_ylabel(value_col, fontsize=12)
        
        # 添加图例
        plt.legend(title=subcategory_col, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 显示图表
        plt.tight_layout()
        plt.show()

    # 生成饼图
    elif chart_type == 'pie':
        # 计算每个类别的总值
        category_totals = data.groupby(category_col)[value_col].sum()
        
        # 绘制饼图
        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Blues", len(category_totals)))
        
        # 设置标题
        ax.set_title('饼图示例', fontsize=16)
        
        # 设置文本大小
        for text in texts + autotexts:
            text.set_fontsize(12)
        
        # 显示图表
        plt.tight_layout()
        plt.show()

    else:
        raise ValueError(f"不支持的图表类型: {chart_type}")

# 测试函数
def test_plot_chart():
    # 测试堆积柱状图
    print("生成堆积柱状图...")
    plot_chart(data, chart_type='stacked_bar', category_col='Category', subcategory_col='Subcategory', value_col='Value')
    
    # 测试饼图
    print("生成饼图...")
    plot_chart(data, chart_type='pie', category_col='Category', value_col='Value')

# 调用测试函数
test_plot_chart()
