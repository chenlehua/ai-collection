# 2023-11-03T12:00:01Z INFO /api/data 200 123ms
# 2023-11-03T12:00:02Z ERROR /api/data 500 456ms
# 2023-11-03T12:00:03Z INFO /api/login 200 78ms
# ...

import re
from collections import defaultdict

def parse_logs(log_file):
    pattern = re.compile(r'(\S+) (\S+) (\S+) (\d+) (\d+)ms')
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                timestamp, level, endpoint, status_code, response_time = match.groups()
                logs.append({
                    'timestamp': timestamp,
                    'level': level,
                    'endpoint': endpoint,
                    'status_code': int(status_code),
                    'response_time': int(response_time)
                })
    return logs

def analyze_logs(logs):
    error_counts = defaultdict(int)
    slow_requests = []
    endpoint_stats = defaultdict(lambda: {
        'total': 0,
        'errors': 0,
        'total_time': 0,
        'max_time': 0
    })
    
    for log in logs:
        endpoint = log['endpoint']
        endpoint_stats[endpoint]['total'] += 1
        endpoint_stats[endpoint]['total_time'] += log['response_time']
        endpoint_stats[endpoint]['max_time'] = max(
            endpoint_stats[endpoint]['max_time'], 
            log['response_time']
        )
        
        if log['status_code'] >= 500:
            error_counts[endpoint] += 1
            endpoint_stats[endpoint]['errors'] += 1
        if log['response_time'] > 300:
            slow_requests.append(log)
            
    # 使用LLM生成报告
    report = generate_report(error_counts, slow_requests, endpoint_stats)
    print(report)

def generate_report(error_counts, slow_requests, endpoint_stats):
    error_summary = '\n'.join([
        f"端点 {endpoint} 发生 {count} 次错误" 
        for endpoint, count in error_counts.items()
    ])
    
    performance_summary = '\n'.join([
        f"端点 {endpoint}: "
        f"总请求={stats['total']}, "
        f"错误率={stats['errors']/stats['total']*100:.1f}%, "
        f"平均响应时间={stats['total_time']/stats['total']:.0f}ms, "
        f"最大响应时间={stats['max_time']}ms"
        for endpoint, stats in endpoint_stats.items()
    ])

    prompt = f"""
请基于以下系统日志数据生成分析报告：

错误统计：
{error_summary}

性能统计：
{performance_summary}

慢请求详情：
{', '.join([f"{req['endpoint']}({req['response_time']}ms)" for req in slow_requests[:5]])}

请：
1. 总结系统的整体健康状况
2. 分析存在的主要问题
3. 提出具体的优化建议
4. 标识需要重点关注的端点
"""
    return call_llm(prompt)

def call_llm(prompt):
    # 这里调用实际的LLM接口，例如OpenAI的API
    # 为了示例，返回一个固定的字符串
    return "报告分析：/api/data 接口出现多次500错误，可能存在服务器端异常。慢请求主要集中在 /api/data 接口，响应时间超过300ms，建议优化数据库查询或增加缓存。"

if __name__ == "__main__":
    logs = parse_logs('access.log')
    analyze_logs(logs)
