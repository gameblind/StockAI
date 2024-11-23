import requests
import os
import base64

# API 配置信息
api_url = "https://ai.comfly.chat/v1/chat/completions"
api_key = "sk-Yo2e1eiFeFNflZvJ8086A7FcEd994eD29fBaB15dA2311f9a"

# 获取当前脚本所在目录
current_dir = os.path.dirname(__file__)

# 构造本地图片路径
image_path = os.path.join(current_dir, "sample_screenshot.png")

# 检查文件是否存在
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file not found at {image_path}")

# 提示文本
prompt_text = "请分析上传的图片内容，并给出简要总结。"

try:
    # 读取图片并编码为 Base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # 构造请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 构造请求数据
    data = {
        "messages": [
            {"role": "system", "content": "你是一个可以处理图片内容的智能助手。"},
            {"role": "user", "content": f"{prompt_text}\n\n图片的Base64编码如下：\n{encoded_image[:100]}..."}
        ],
        "model": "gpt-4-all"  # 替换为支持的模型名称
    }

    # 发送 POST 请求
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()  # 检查是否有 HTTP 错误

    # 打印返回结果
    print("API Response:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")