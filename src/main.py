import json
import os
from pynput import keyboard
from src.screenshot.screen_capture import capture_fullscreen
from src.ocr.ocr_processor import extract_text_from_image, extract_stock_info

# 加载配置文件
def load_settings(config_path="config/setting.json"):
    """
    加载配置文件
    Args:
        config_path (str): 配置文件路径
    Returns:
        dict: 配置文件的内容
    """
    try:
        with open(config_path, "r") as f:
            print(f"成功加载配置文件: {config_path}")
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到，请确保配置文件存在")
        raise
    except json.JSONDecodeError as e:
        print(f"配置文件 {config_path} 格式错误: {e}")
        raise

def trigger_screenshot_and_recognize(settings):
    """
    快捷键触发截图并识别内容
    Args:
        settings (dict): 配置文件内容
    """
    print("快捷键触发截图并识别内容...")
    screenshot_folder = settings.get("screenshot_folder", "screenshots")
    screenshot_path = capture_fullscreen(screenshot_folder)
    if screenshot_path and screenshot_path.endswith((".png", ".jpg", ".jpeg")):
        print(f"截图成功，保存路径: {screenshot_path}")

        # 使用 OCR 识别图像内容
        ocr_language = settings.get("ocr_language", "eng+chi_sim")
        text = extract_text_from_image(screenshot_path, ocr_language)
        if text:
            print("提取的文本内容：")
            print(text)

            # 提取股票信息
            stock_info = extract_stock_info(text)
            if stock_info:
                print("解析的股票信息：")
                print(stock_info)
            else:
                print("未能解析出有效的股票信息")
        else:
            print("未能提取到文本内容")
    else:
        print("截图失败：未生成有效文件！")

def bind_shortcut(shortcut, action):
    """
    绑定快捷键
    Args:
        shortcut (str): 快捷键组合，例如 'ctrl+shift+i'
        action (function): 要绑定的函数
    """
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

def main():
    """
    主程序入口
    """
    print("StockAI 启动...")

    # 加载配置
    settings = load_settings()

    # 获取快捷键配置
    screenshot_shortcut = settings.get("shortcuts", {}).get("screenshot", "ctrl+shift+i")

    print(f"绑定截图快捷键为: {screenshot_shortcut}")
    bind_shortcut(screenshot_shortcut, lambda: trigger_screenshot_and_recognize(settings))

    # 防止主线程退出
    print("按下 Ctrl+C 退出程序")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n程序退出")

if __name__ == "__main__":
    main()