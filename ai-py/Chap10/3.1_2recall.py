# 评估检索召回效果
from langchain_community.llms.tongyi import Tongyi
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_recall,context_precision
import pandas as pd

data_samples = {
    'question': [
            '公司的年假政策是怎样的？',
            '公司的年假政策是怎样的？',
            '公司的年假政策是怎样的？'
        ],
    'answer': [
            '公司员工每年可以享受5天带薪年假。',  # 部分正确
            '公司正式员工工作满一年后可以享受7天带薪年假，工作满三年后每年增加1天，最多不超过15天。',  # 完全正确
            '我们公司没有固定的年假政策。'  # 错误答案
        ],
    'ground_truth': [
            '公司正式员工工作满一年后可以享受7天带薪年假，工作满三年后每年增加1天，最多不超过15天。'
        ] * 3,
    'contexts' : [
        [
            '公司正式员工工作满一年后可以享受7天带薪年假，工作满三年后每年增加1天，最多不超过15天。',
            '员工福利政策包括带薪年假、节日福利等。',
            '新入职员工试用期为3个月。'
        ],
        [
            '工作满三年后每年增加1天，最多不超过15天。',
            '员工福利政策包括带薪年假、节日福利等。',
            '年假使用规定：员工应提前3个工作日提交年假申请，经直属领导审批后方可休假。',
            '未休完的年假可以顺延至次年第一季度使用，逾期作废。'
        ],
        [
            '公司每年组织团建活动。',
            '员工可以享受带薪病假。',
            '公司提供餐补和交通补贴。'
        ]
    ],
}

# 修改评估方式，添加更细致的上下文相关性判断
try:
    dataset = Dataset.from_dict(data_samples)
    scores = evaluate(
        dataset = dataset,
        metrics=[
            context_recall,  # 移除括号和参数
            context_precision
        ],
        llm=Tongyi(model_name="qwen-plus")
    )
    
    # 转换为DataFrame并优化显示
    results_df = scores.to_pandas()
    
    print("\n=== 评估结果明细 ===")
    for i in range(len(data_samples['question'])):
        print(f"\n对话 {i+1}:")
        print(f"问题: {data_samples['question'][i]}")
        print(f"回答: {data_samples['answer'][i]}")
        print(f"参考答案: {data_samples['ground_truth'][i]}")
        print("上下文相关性分析:")
        for ctx in data_samples['contexts'][i]:
            print(f"- {ctx}")
        print(f"上下文召回率: {results_df.iloc[i]['context_recall']:.3f}")
        print(f"上下文精确率: {results_df.iloc[i]['context_precision']:.3f}")
        print("-" * 60)
    
    print("\n=== 整体评估结果 ===")
    print(f"平均上下文召回率: {results_df['context_recall'].mean():.3f}")
    print(f"平均上下文精确率: {results_df['context_precision'].mean():.3f}")

except Exception as e:
    print(f"评估过程中出现错误: {str(e)}")