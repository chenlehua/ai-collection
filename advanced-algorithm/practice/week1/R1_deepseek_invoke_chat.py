# pip3 install openai

from openai import OpenAI

client = OpenAI(api_key="sk-35f1fa6351f049b9bfc00d31d575b218", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
