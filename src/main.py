import json
from pynput import keyboard
from src.screenshot.screen_capture import capture_fullscreen

# 加载快捷键配置
def load_shortcuts(config_path="config/shortcuts.json"):
    """
    加载快捷键配置文件
    Args:
        config_path (str): 配置文件路径
    Returns:
        dict: 包含快捷键配置的字典
    """
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到，使用默认快捷键")
        return {"screenshot": "ctrl+shift+i"}

# 截图触发逻辑

def trigger_screenshot():
    print("快捷键触发截图...")
    screenshot_path = capture_fullscreen()
    if screenshot_path:
        print(f"截图成功，保存路径: {screenshot_path}")
    else:
        print("截图失败！")

# 监听逻辑
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
    print("StockAI 启动...")

    # 加载快捷键配置
    shortcuts = load_shortcuts()
    screenshot_shortcut = shortcuts.get("screenshot", "ctrl+shift+i")

    print(f"绑定截图快捷键为: {screenshot_shortcut}")
    bind_shortcut(screenshot_shortcut, trigger_screenshot)

    # 防止主线程退出
    print("按下 Ctrl+C 退出程序")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n程序退出")

if __name__ == "__main__":
    main()