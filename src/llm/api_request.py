import requests
from settings import CONFIG_MANAGER

def submit_request_to_api(model_name, prompt_text, image_url):
    """
    提交请求到 AI API，分析图片内容。

    Args:
        model_name (str): 模型名称（如 "gpt-4-all"）。
        prompt_text (str): 提示词。
        image_url (str): 图片的 URL。

    Returns:
        dict: AI API 的响应结果。
    """
    # 从配置文件加载 API 配置信息
    api_key = CONFIG_MANAGER.get("api_config").get("api_key")
    api_url = CONFIG_MANAGER.get("api_config").get("api_url")

    # 构造请求头和数据
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "你是一个可以处理图片内容的智能助手。"},
            {"role": "user", "content": f"{prompt_text}\n{image_url}"}
        ],
        "model": model_name
    }

    # 发送请求到 AI API
    response = requests.post(f"{api_url}/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# 测试代码（如果需要单独运行此模块）
if __name__ == "__main__":
    # 示例：模型名称、提示词、图片 URL
    model_name = "gpt-4-all"
    prompt_text = "请分析以下图片内容，并总结图片的核心信息："
    image_url = "https://raw.githubusercontent.com/gameblind/image-storage/main/images/sample_screenshot.png"

    try:
        result = submit_request_to_api(model_name, prompt_text, image_url)
        print("AI API Response:", result)
    except Exception as e:
        print(f"An error occurred: {e}")