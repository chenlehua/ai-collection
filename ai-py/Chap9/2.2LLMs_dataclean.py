from openai import OpenAI
import json
from typing import List, Dict
import os

def read_file(file_path: str) -> List[str]:
    """
    读取文本文件并返回内容列表
    
    Args:
        file_path (str): 输入文件的路径
        
    Returns:
        List[str]: 包含文件内容的列表。如果文件为空或发生错误，返回空列表
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
        
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
        if not content:
            return []
            
        return [content] if content.strip() else []
    except Exception as e:
        print(f"读取文件时发生未知错误: {str(e)}")
        raise


def process_conversation(segments: List[str], api_key: str, base_url: str) -> List[Dict]:
    """
    处理对话并返回结构化数据
    """
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # 修改 prompt，要求输出完整的JSON数组格式
        prompt = """请将以下内容转换为问答对话格式的JSON数组。要求：
1. 输出格式必须是JSON数组
2. 每个问答对包含instruction(问题)、input(空字符串)和output(答案)
3. 不要输出任何markdown标记
4. 确保输出是有效的JSON格式

示例输入：世界上最高的山是什么，珠穆朗玛峰是世界最高峰。
示例输出：
[
  {
    "instruction": "世界上最高的山是什么？",
    "input": "",
    "output": "珠穆朗玛峰是世界最高峰。"
  }
]

请按照上述格式处理以下内容："""
        
        conversation_data = []
        for segment in segments:
            if not segment.strip():
                continue
                
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": segment}
            ]
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages
            )
            
            try:
                ai_response = response.choices[0].message.content.strip()
                # 移除可能存在的markdown标记
                ai_response = ai_response.replace('```json', '').replace('```', '').strip()
                parsed_response = json.loads(ai_response)
                
                # 确保解析后的数据是列表格式
                if isinstance(parsed_response, list):
                    conversation_data.extend(parsed_response)
                else:
                    print(f"跳过无效格式的响应: {ai_response}")
                    
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")
                print(f"原始响应: {ai_response}")
                continue
            
        return conversation_data
        
    except Exception as e:
        print(f"处理对话错误: {str(e)}")
        return []

def main():
    # 从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = "https://api.deepseek.com"
    
    file_path = "D:\\a.txt"  # 建议通过参数传入
    
    # 读取文件
    segments = read_file(file_path)
    if not segments:
        print("没有读取到有效内容")
        return
        
    # 处理对话
    conversation_data = process_conversation(segments, api_key, base_url)
    
    # 保存结果
    if conversation_data:
        with open("conversation_output.json", "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            
if __name__ == "__main__":
    main()

