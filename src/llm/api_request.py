import requests
import os
import json
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# 使用相对路径加载配置文件
def load_config():
    """
    加载配置文件
    """
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/settings.json"))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)

CONFIG = load_config()

def submit_request_to_api(model_name, prompt_text, image_url, settings):
    """
    提交请求到 AI API，分析图片内容。
    Args:
        model_name (str): 大模型名称。
        prompt_text (str): 提示词。
        image_url (str): 图片 URL。
        settings (dict): 配置字典。
    Returns:
        dict: 大模型返回的 JSON 结果。
    """
    api_key = settings.get("api_config", {}).get("api_key")
    api_url = settings.get("api_config", {}).get("api_url")

    # 从配置中获取系统角色提示词
    system_prompt = settings.get("prompts", {}).get(
        "system_role",
        "你是一个股票分析师具备非常强的股票交易能力，可以看懂图片，识别股票信息和预判股票走势。"
    )

    # 构造请求头和数据
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{prompt_text}\n{image_url}"}
        ],
        "model": model_name
    }

    try:
        print(f"向大模型发送请求: {data}")
        response = requests.post(f"{api_url}/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print(f"大模型返回的原始结果: {result}")
        return result
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        raise

import re

def extract_stock_info_from_model(model_result):
    """
    从大模型返回的结果中提取股票信息。
    Args:
        model_result (dict): 大模型返回的完整结果。
    Returns:
        dict: 提取的股票信息，包括代码、名称和K线种类。
    """
    try:
        # 获取内容
        content = model_result["choices"][0]["message"]["content"]

        # 使用正则提取股票信息
        stock_code_match = re.search(r"股票代码[：:]\s*(\d{6})", content)
        stock_name_match = re.search(r"股票名称[：:]\s*(.+?)\s*(?:[,\n]|$)", content)
        kline_type_match = re.search(r"K线种类[：:]\s*(.+?)\s*(?:[,\n]|$)", content)

        stock_code = stock_code_match.group(1) if stock_code_match else None
        stock_name = stock_name_match.group(1).strip() if stock_name_match else "未知"
        kline_type = kline_type_match.group(1).strip() if kline_type_match else "未知"

        return {
            "code": stock_code,
            "name": stock_name,
            "kline_type": kline_type,
        }
    except Exception as e:
        print(f"解析大模型结果出错: {e}")
        return None

if __name__ == "__main__":
    # 测试提交请求和解析
    test_settings = CONFIG
    test_model_name = "gpt-4-all"
    test_prompt_text = "从图片中识别出，股票代码，股票名称，K线种类，并分析股票相关信息。"
    test_image_url = "https://example.com/test_image.png"

    try:
        # 提交请求到大模型
        model_result = submit_request_to_api(test_model_name, test_prompt_text, test_image_url, test_settings)
        
        # 解析结果
        stock_info = extract_stock_info_from_model(model_result)
        if stock_info:
            print(f"提取的股票信息: {stock_info}")
        else:
            print("未能提取到股票信息")
    except Exception as e:
        print(f"运行出错: {e}")