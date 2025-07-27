import pandas as pd
import numpy as np
import re
from transformers import pipeline

# 示例数据：包含患者的病历记录、诊断信息和实验室结果
data = pd.DataFrame({
    'Patient_ID': [1, 2, 3, 4],
    'Medical_Record': [
        "Patient complains of headache and nausea. Prescribed ibuprofen. Follow-up in 2 weeks.",
        "Patient reports chest pain. ECG normal. Prescribed aspirin. Follow-up in 1 week.",
        "Patient has a history of diabetes. Blood sugar levels elevated. Prescribed insulin.",
        "Patient reports dizziness. MRI shows no abnormalities. Prescribed rest."
    ],
    'Lab_Results': [
        "Blood Pressure: 120/80, Blood Sugar: 90 mg/dL",
        "Blood Pressure: 130/85, Blood Sugar: 110 mg/dL",
        "Blood Pressure: 140/90, Blood Sugar: 200 mg/dL",
        np.nan  # 缺失值
    ],
    'Diagnosis': [
        "Headache, Nausea",
        "Chest Pain",
        "Diabetes",
        "Dizziness"
    ]
})

# 1. 长文本处理：提取医疗文本中的关键信息
# 使用 Hugging Face 的 transformers 库
# 加载预训练的 BART 模型（facebook/bart-large-cnn），
# 并通过 pipeline 提供的摘要功能提取病历记录中的关键信息。
# 该模型能够自动生成病历的简短摘要，
# 帮助过滤无效信息并提取关键信息。
def extract_key_information(text, model):
    """
    使用 LLM 提取医疗文本中的关键信息。
    
    :param text: 输入的医疗文本
    :param model: 预训练的 LLM 模型
    :return: 提取的关键信息
    """
    # 使用 LLM 模型进行文本摘要
    summary = model(text, max_length=50, min_length=10, do_sample=False)
    return summary[0]['summary_text']

# 2. 半结构化数据处理：将实验室结果转换为结构化格式
# 使用正则表达式提取实验室结果中的血压和血糖值，
# 并将其转换为结构化格式。
# 如果实验室结果缺失，则返回 NaN，以便后续处理。
def process_lab_results(lab_results):
    """
    将实验室结果从半结构化格式转换为结构化格式。
    
    :param lab_results: 实验室结果的文本
    :return: 结构化的实验室结果
    """
    if pd.isna(lab_results):
        return np.nan, np.nan
    
    # 使用正则表达式提取血压和血糖值
    bp_match = re.search(r'Blood Pressure: (\d+/\d+)', lab_results)
    sugar_match = re.search(r'Blood Sugar: (\d+) mg/dL', lab_results)
    
    blood_pressure = bp_match.group(1) if bp_match else np.nan
    blood_sugar = int(sugar_match.group(1)) if sugar_match else np.nan
    
    return blood_pressure, blood_sugar

# 3. 缺失值处理：智能填充缺失的实验室结果
# 对于缺失的血压，使用众数（最常见的值）进行填充；
# 对于缺失的血糖值，使用均值进行填充。
# 这种方法确保了数据的完整性，同时避免了因缺失值导致的分析偏差。
def handle_missing_values(data):
    """
    处理缺失值，使用均值填充缺失的实验室结果。
    
    :param data: 输入数据
    :return: 处理后的数据
    """
    # 填充缺失的血压和血糖值
    data['Blood_Pressure'].fillna(data['Blood_Pressure'].mode()[0], inplace=True)
    data['Blood_Sugar'].fillna(data['Blood_Sugar'].mean(), inplace=True)
    
    return data

# 4. 数据标准化：统一数据格式
# 将血压数据拆分为收缩压（Systolic BP）和舒张压（Diastolic BP）两列，
# 并将其转换为整数类型。
# 这种标准化操作有助于后续的分析和建模。
def standardize_data(data):
    """
    统一数据格式，例如将血压转换为 systolic/diastolic 格式。
    
    :param data: 输入数据
    :return: 标准化后的数据
    """
    # 将血压转换为 systolic 和 diastolic 两列
    data[['Systolic_BP', 'Diastolic_BP']] = data['Blood_Pressure'].str.split('/', expand=True)
    data['Systolic_BP'] = data['Systolic_BP'].astype(int)
    data['Diastolic_BP'] = data['Diastolic_BP'].astype(int)
    
    # 删除原始的 Blood_Pressure 列
    data.drop(columns=['Blood_Pressure'], inplace=True)
    
    return data

# 5. 无效信息过滤：删除重复记录
def remove_duplicates(data):
    """
    删除重复的记录。
    
    :param data: 输入数据
    :return: 去重后的数据
    """
    return data.drop_duplicates()

# 测试医疗数据清洗流程
def clean_medical_data(data):
    # 加载预训练的 LLM 模型（使用 Hugging Face 的 transformers 库）
    summarization_model = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # 处理长文本：提取病历记录中的关键信息
    data['Key_Information'] = data['Medical_Record'].apply(lambda x: extract_key_information(x, summarization_model))
    
    # 处理半结构化数据：将实验室结果转换为结构化格式
    data[['Blood_Pressure', 'Blood_Sugar']] = data['Lab_Results'].apply(lambda x: pd.Series(process_lab_results(x)))
    
    # 处理缺失值
    data = handle_missing_values(data)
    
    # 数据标准化
    data = standardize_data(data)
    
    # 删除无效信息（如重复记录）
    data = remove_duplicates(data)
    
    return data

# 清洗数据
cleaned_data = clean_medical_data(data)

# 查看清洗后的数据
print("\n清洗后的数据：")
print(cleaned_data)
