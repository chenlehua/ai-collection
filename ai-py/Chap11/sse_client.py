import requests

def sse_client():
    url = "http://localhost:8000/sse"
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        buffer = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                # 只处理以 "data: " 开头的行
                if line.startswith('data: '):
                    message = line.replace('data: ', '').strip()
                    if message:  # 确保消息不为空
                        print(f"收到消息: {message}")
    else:
        print(f"连接失败，状态码: {response.status_code}")

if __name__ == "__main__":
    print("开始连接 SSE 服务器...")
    try:
        sse_client()
    except KeyboardInterrupt:
        print("\n已停止客户端")
    except Exception as e:
        print(f"发生错误: {e}")