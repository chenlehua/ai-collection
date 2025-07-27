# 评估 RAG 应用回答质量
# Answer Correctness 的得分 = 0.25 * 语义相似度得分 + 0.75 * 事实准确度得分
from langchain_community.llms.tongyi import Tongyi
from langchain_community.embeddings import DashScopeEmbeddings
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness
from typing import Dict, List
import logging
import pandas as pd
def create_evaluation_dataset(data: Dict[str, List[str]]) -> Dataset:
    """创建评估数据集"""
    try:
        return Dataset.from_dict(data)
    except Exception as e:
        logging.error(f"创建数据集时出错: {str(e)}")
        raise

def evaluate_answers(dataset: Dataset) -> pd.DataFrame:
    """评估答案正确性"""
    try:
        llm = Tongyi(model_name="qwen-plus")
        embeddings = DashScopeEmbeddings(model="text-embedding-v2")
        
        score = evaluate(
            dataset=dataset,
            metrics=[answer_correctness],
            llm=llm,
            embeddings=embeddings
        )
        return score.to_pandas()
    except Exception as e:
        logging.error(f"评估过程中出错: {str(e)}")
        raise

def main():
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    

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
        ] * 3
    }
    
    try:
        dataset = create_evaluation_dataset(data_samples)
        results = evaluate_answers(dataset)
        
        # 重置索引从1开始
        results_display = results[['question', 'answer', 'answer_correctness']].reset_index(drop=True)
        results_display.index = results_display.index + 1  # 索引加1
        
        # 美化输出
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print("\n评估结果：")
        print(results_display)
        

        print("\n分析说明：")
        print(f"1号答案 (部分正确) 得分: {results_display.loc[1, 'answer_correctness']:.3f}")
        print(f"2号答案 (完全正确) 得分: {results_display.loc[2, 'answer_correctness']:.3f}")
        print(f"3号答案 (完全错误) 得分: {results_display.loc[3, 'answer_correctness']:.3f}")
        
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()