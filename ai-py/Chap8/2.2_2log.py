# log_analyzer.py

import glob
import re
import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import os

def load_logs(log_directory):
    logs = []
    for logfile in glob.glob(f"{log_directory}/*.log"):
        with open(logfile, 'r') as f:
            logs.extend(f.readlines())
    return logs

def parse_logs(logs):
    error_pattern = re.compile(r'ERROR - \[Thread-(\d+)\] Exception in (\w+): (.*)')
    error_dict = defaultdict(list)
    for line in logs:
        match = error_pattern.search(line)
        if match:
            thread_id, func_name, error_msg = match.groups()
            error_dict[func_name].append({
                'thread_id': thread_id,
                'error_msg': error_msg,
                'timestamp': extract_timestamp(line)
            })
    return error_dict

def extract_timestamp(log_line):
    # 提取日志行中的时间戳
    timestamp_str = log_line.split(' - ')[0]
    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')

def generate_visual_report(error_dict):
    print("开始生成可视化报告...")
    try:
        # 检查输入数据
        print(f"接收到的错误数据: {dict(error_dict)}")
        
        # 设置中文字体支持
        print("设置matplotlib参数...")
        try:
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
        except Exception as e:
            print(f"设置字体时出错: {e}")
        
        # 创建新的图形
        print("创建图形...")
        fig = plt.figure(figsize=(10, 6))
        
        # 准备数据
        func_names = list(error_dict.keys())
        error_counts = [len(errors) for errors in error_dict.values()]
        print(f"函数名称: {func_names}")
        print(f"错误计数: {error_counts}")
        
        # 绘制柱状图
        print("绘制柱状图...")
        bars = plt.bar(func_names, error_counts, color='lightcoral')
        
        # 添加标签
        plt.xlabel('函数名称')
        plt.ylabel('错误次数')
        plt.title('各函数错误统计')
        
        # 保存图片
        print("尝试保存图片...")
        save_path = 'error_report.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图片已保存到: {os.path.abspath(save_path)}")
        
        plt.close()
        
    except Exception as e:
        print(f"生成可视化报告时发生错误: {e}")
        import traceback
        print(traceback.format_exc())
    
    # 输出文本报告
    print("\n=== 错误统计报告 ===")
    for func_name, errors in error_dict.items():
        print(f"函数 {func_name} 发生异常 {len(errors)} 次")
        for error in errors:
            print(f" - [线程{error['thread_id']}] 时间: {error['timestamp']}, 错误信息: {error['error_msg']}")

# 主函数
if __name__ == "__main__":
    # 使用内置的测试日志数据
    test_logs = [
        "2024-03-20 10:15:23,456 - ERROR - [Thread-1] Exception in process_data: IndexError: list index out of range",
        "2024-03-20 10:15:24,789 - INFO - [Thread-2] Successfully processed item 1",
        "2024-03-20 10:15:25,123 - ERROR - [Thread-3] Exception in save_to_database: TypeError: cannot concatenate str and int objects",
        "2024-03-20 10:15:26,456 - ERROR - [Thread-1] Exception in process_data: ValueError: invalid literal for int()",
        "2024-03-20 10:15:27,789 - INFO - [Thread-4] Normal operation completed",
        "2024-03-20 10:15:28,012 - ERROR - [Thread-5] Exception in validate_input: KeyError: 'user_id' not found"
    ]
    
    # 修改load_logs调用
    # logs = load_logs('logs')  # 注释掉原来的代码
    error_dict = parse_logs(test_logs)  # 直接使用测试日志
    generate_visual_report(error_dict)
