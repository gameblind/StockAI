import requests
import json

url = "https://ai.comfly.chat/v1/chat/completions"

payload = json.dumps({
   "model": "gpt-3.5-turbo",
   "messages": [
      {
         "role": "system",
         "content": "You are a helpful assistant."
      },
      {
         "role": "user",
         "content": "Hello!"
      }
   ]
})
headers = {
   'Accept': 'application/json',
   'Authorization': 'Bearer sk-Yo2e1eiFeFNflZvJ8086A7FcEd994eD29fBaB15dA2311f9a',
   'Content-Type': 'application/json'
}

# 打印调试信息
print("=== Debug Information ===")
print("URL:", url)
print("Headers:", headers)
print("Payload:", payload)
print("==========================")

try:
    # 发送请求
    response = requests.request("POST", url, headers=headers, data=payload)

    # 打印HTTP响应状态码
    print("HTTP Status Code:", response.status_code)

    # 检查是否响应成功
    if response.status_code == 200:
        print("Response Data:", response.json())
    else:
        print("Error Response:", response.text)

except requests.exceptions.RequestException as e:
    # 捕获所有请求相关的错误
    print(f"Request Exception: {e}")