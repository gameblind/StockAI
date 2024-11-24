import json
import os
import datetime
import re
import sys

# 添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pynput import keyboard
from src.screenshot.screen_capture import capture_fullscreen
from src.upload_images.upload_images import upload_image_to_github
from src.llm.api_request import submit_request_to_api, extract_stock_info_from_model
from src.ocr.ocr_processor import extract_text_from_image, extract_stock_info
from src.data_fetcher.fetch_data_by import fetch_historical_data, save_data_to_file
# 加载配置文件
def load_settings(config_path="config/settings.json"):
    try:
        with open(config_path, "r") as f:
            print(f"成功加载配置文件: {config_path}")
            settings = json.load(f)

            # 设置默认值
            settings.setdefault("prompts", {})
            settings["prompts"].setdefault("system_role", "你是一个股票分析师具备非常强的股票交易能力，可以看懂图片，识别股票信息和预判股票走势。")
            settings["prompts"].setdefault("image_recognition", "从图片中识别出，股票代码，股票名称，股票k线种类（如几日k线，分时线，60分钟线等），并帮我分析图中股票的相关信息做出预测：")
            return settings
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到，请确保配置文件存在")
        raise
    except json.JSONDecodeError as e:
        print(f"配置文件 {config_path} 格式错误: {e}")
        raise

# 动态生成默认时间范围
def get_default_date_range():
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    return start_date, end_date

# Step 1: 截图
def take_screenshot(settings):
    screenshot_folder = settings.get("screenshot_folder", "screenshots")
    screenshot_path = capture_fullscreen(screenshot_folder)
    if not screenshot_path or not os.path.exists(screenshot_path):
        raise Exception("截图失败，未生成有效文件")
    print(f"截图成功，保存路径: {screenshot_path}")
    return screenshot_path

# Step 2: 上传截图到 GitHub
def upload_to_github(screenshot_path, settings):
    upload_path = f"images/{os.path.basename(screenshot_path)}"
    try:
        image_url = upload_image_to_github(screenshot_path, upload_path)
        print(f"图片已成功上传到 GitHub，URL: {image_url}")
        return image_url
    except Exception as e:
        raise Exception(f"图片上传失败: {e}")

# Step 3: 调用大模型
def call_ai_api(image_url, settings):
    """
    调用大模型，分析图像内容。
    """
    model_name = settings.get("model_name", "gpt-4-all")
    # 从配置中获取用户提示词
    prompt_text = settings.get("prompts", {}).get(
        "image_recognition",
        "从图片中识别出，股票代码，股票名称，股票k线种类（如几日k线，分时线，60分钟线等），并帮我分析图中股票的相关信息做出预测："
    )
    try:
        print("调用大模型进行分析...")
        result = submit_request_to_api(model_name, prompt_text, image_url, settings)
        print("大模型返回结果：", result)
        return result
    except Exception as e:
        raise Exception(f"调用大模型失败: {e}")
    

# Step 4: 本地 OCR 识别
def perform_ocr(screenshot_path, settings):
    ocr_language = settings.get("ocr_language", "eng+chi_sim")
    text = extract_text_from_image(screenshot_path, ocr_language)
    if not text:
        raise Exception("OCR 未能提取到文本内容")
    print("OCR 提取的文本内容：")
    print(text)
    stock_info = extract_stock_info(text)
    if stock_info:
        print("解析的股票信息：", stock_info)
    else:
        print("OCR 未能解析出有效的股票信息")
    return text, stock_info

# Step 5: 分析结果并获取股票历史数据
import re

def analyze_data(model_result, ocr_text, settings):
    """
    综合分析大模型返回内容和OCR提取的股票信息。
    Args:
        model_result (dict): 大模型返回的原始结果。
        ocr_text (str): OCR 提取的文本内容。
        settings (dict): 配置字典。
    """
    print("\n=== 综合分析结果 ===")
    print(f"大模型返回的原始结果：\n{model_result}")

    # 从大模型结果中提取股票信息
    try:
        stock_info_from_model = extract_stock_info_from_model(model_result)
        if stock_info_from_model:
            print(f"从大模型解析出的股票信息：")
            # 使用正则提取6位数字股票代码
            stock_code = re.search(r"\b\d{6}\b", stock_info_from_model.get("code", ""))
            stock_code = stock_code.group() if stock_code else None
            stock_name = stock_info_from_model.get("name", "未知")
            kline_type = stock_info_from_model.get("kline_type", "未知")
            print(f"股票代码：{stock_code}")
            print(f"股票名称：{stock_name}")
            print(f"K线种类：{kline_type}")
        else:
            print("未能从大模型返回内容中提取股票信息。")
            stock_code, stock_name, kline_type = None, None, None
    except Exception as e:
        print(f"解析大模型返回内容时出错：{e}")
        stock_code, stock_name, kline_type = None, None, None

    # 获取历史数据
    if stock_code:
        start_date, end_date = get_default_date_range()
        print(f"尝试获取历史数据，时间范围：{start_date} 至 {end_date}")
        try:
            historical_data = fetch_historical_data(stock_code, start_date=start_date, end_date=end_date)
            if historical_data:
                print(f"获取到 {len(historical_data)} 条历史记录。")
                save_data_to_file(historical_data, settings.get("output_file"))
                print(f"历史数据已保存到文件：{settings.get('output_file')}")
            else:
                print(f"未获取到历史数据，股票代码：{stock_code}")
        except Exception as e:
            print(f"获取历史数据失败: {e}")
    else:
        print("无法获取股票代码，跳过历史数据获取。")


# 主流程：整合各个步骤
def process_workflow(settings):
    print("触发操作流...")
    try:
        # Step 1: 截图
        screenshot_path = take_screenshot(settings)

        # Step 2: 上传截图
        image_url = upload_to_github(screenshot_path, settings)

        # Step 3: 调用大模型
        model_result = call_ai_api(image_url, settings)

        # Step 4: 本地 OCR 识别
        ocr_text, stock_info = perform_ocr(screenshot_path, settings)

        # Step 5: 综合分析结果并获取股票历史数据
        analyze_data(model_result, ocr_text, settings)
    except Exception as e:
        print(f"操作流中发生错误: {e}")

# 绑定快捷键
def bind_shortcut(shortcut, action):
    def parse_key(key_string):
        keys = key_string.lower().split("+")
        parsed_keys = []
        for key in keys:
            if key == "ctrl":
                parsed_keys.append(keyboard.Key.ctrl)
            elif key == "shift":
                parsed_keys.append(keyboard.Key.shift)
            elif len(key) == 1:  # 普通字符键
                parsed_keys.append(keyboard.KeyCode.from_char(key))
        return parsed_keys

    shortcut_keys = parse_key(shortcut)
    current_keys = set()

    def on_press(key):
        current_keys.add(key)
        if all(k in current_keys for k in shortcut_keys):
            action()

    def on_release(key):
        if key in current_keys:
            current_keys.remove(key)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

# 主程序入口
def main():
    print("StockAI 启动...")

    # 加载配置
    settings = load_settings()

    # 获取快捷键配置
    screenshot_shortcut = settings.get("shortcuts", {}).get("screenshot", "ctrl+shift+i")
    print(f"绑定截图快捷键为: {screenshot_shortcut}")

    # 绑定快捷键，触发操作流
    bind_shortcut(screenshot_shortcut, lambda: process_workflow(settings))

    # 防止主线程退出
    print("按下 Ctrl+C 退出程序")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n程序退出")

if __name__ == "__main__":
    main()