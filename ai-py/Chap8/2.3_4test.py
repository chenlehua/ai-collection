import unittest
import subprocess
from typing import Dict, Any
import sys

def mock_llm_response(prompt: str) -> str:
    """模拟LLM响应，用于演示"""
    if "生成测试用例" in prompt:
        return """
import unittest

class TestComplexFunction(unittest.TestCase):
    def test_normal_input(self):
        '''测试普通输入'''
        self.assertEqual(complex_function(2, 3), 1.67)  # (2+3)/(2*3) = 5/6 ≈ 1.67
        
    def test_negative_numbers(self):
        '''测试负数输入'''
        self.assertEqual(complex_function(-2, -3), 1.67)  # (-2+-3)/(-2*-3) = -5/6
        
    def test_zero_division(self):
        '''测试除零情况'''
        with self.assertRaises(ValueError):
            complex_function(0, 0)
            
    def test_large_numbers(self):
        '''测试大数'''
        self.assertEqual(complex_function(1000, 2000), 0.0015)  # (1000+2000)/(1000*2000)

if __name__ == '__main__':
    unittest.main()
"""
    elif "分析" in prompt:
        return """
测试失败分析：
1. 失败原因：
   - 函数在处理除数为零的情况时没有进行适当的错误处理
   - 当 a=0 且 b=0 时，计算 c/d 会导致 ZeroDivisionError

2. 修复建议：
   - 在函数开始处添加对除数为零的检查
   - 当检测到可能的除零情况时，抛出 ValueError 异常
   - 建议修改代码如下：
   
   def complex_function(a, b):
       if a * b == 0:
           raise ValueError("除数不能为零")
       c = a + b
       d = a * b
       return c / d
"""
    return "模拟LLM响应"

def generate_test_cases(function_name: str, code: str) -> str:
    """生成测试用例"""
    prompt = f"""
请为以下函数生成全面的测试用例，包括:
1. 正常输入测试
2. 边界值测试
3. 异常情况测试
4. 特殊值测试

函数名：{function_name}
代码：
{code}
"""
    return mock_llm_response(prompt)

def analyze_test_failure(test_result: str, function_name: str, code: str) -> str:
    """分析测试失败原因"""
    prompt = f"""
请分析以下测试失败的原因：

函数名：{function_name}
代码：
{code}

测试结果：
{test_result}
"""
    return mock_llm_response(prompt)

def complex_function(a: float, b: float) -> float:
    """示例函数：计算 (a+b)/(a*b)"""
    c = a + b
    d = a * b
    return c / d

def run_demo():
    """运行演示程序"""
    print("=== 自动化测试演示程序 ===\n")
    
    # 显示原始函数
    print("待测试函数：")
    print(complex_function.__doc__)
    print("\n函数代码：")
    print(inspect.getsource(complex_function))
    
    # 生成测试用例
    print("\n正在生成测试用例...")
    test_cases = generate_test_cases('complex_function', inspect.getsource(complex_function))
    print("\n生成的测试用例：")
    print(test_cases)
    
    # 保存测试用例
    test_file = 'test_complex_function.py'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(f"from __main__ import complex_function\n")
        f.write(test_cases)
    
    # 运行测试
    print("\n开始运行测试...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("\n测试失败！")
            print("错误信息：")
            print(result.stderr)
            
            print("\n正在分析失败原因...")
            analysis = analyze_test_failure(result.stderr, 'complex_function', 
                                         inspect.getsource(complex_function))
            print("\n分析结果：")
            print(analysis)
        else:
            print("\n所有测试通过！")
            
    except Exception as e:
        print(f"\n运行测试时发生错误: {str(e)}")
    
    # 清理测试文件
    import os
    try:
        os.remove(test_file)
        if os.path.exists('__pycache__'):
            import shutil
            shutil.rmtree('__pycache__')
    except:
        pass

if __name__ == "__main__":
    import inspect
    run_demo()
