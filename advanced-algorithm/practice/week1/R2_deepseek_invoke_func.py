# pip3 install openai
from openai import OpenAI

client = OpenAI(api_key="sk-35f1fa6351f049b9bfc00d31d575b218", base_url="https://api.deepseek.com")

tools = [
    {
        "type": "function",
        "function": {
            "name": "Ticket",
            "description": "根据用户提供的信息查询火车时刻",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "description": "要查询的火车日期",
                        "title": "Date",
                        "type": "string",
                    },
                    "departure": {
                        "description": "出发城市或车站",
                        "title": "Departure",
                        "type": "string",
                    },
                    "destination": {
                        "description": "目的城市或车站",
                        "title": "Destination",
                        "type": "string",
                    },
                },
                "required": ["date", "departure", "destination"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你能帮我查一下2024年1月1日从北京南站到上海的火车票吗？"},
    ],
    tools=tools,
    stream=False
)

print(response.choices[0].message.tool_calls)
