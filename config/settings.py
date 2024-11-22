import os
import json

def load_config(config_path="config/api_config.json"):
    """加载配置文件"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)

def update_shortcut(key_name, new_shortcut, config_path="config/shortcuts.json"):
    """
    更新快捷键配置
    Args:
        key_name (str): 要修改的快捷键名称（如 'screenshot'）
        new_shortcut (str): 新的快捷键组合（如 'ctrl+shift+s'）
        config_path (str): 配置文件路径
    """
    try:
        with open(config_path, "r") as f:
            shortcuts = json.load(f)
    except FileNotFoundError:
        shortcuts = {}

    shortcuts[key_name] = new_shortcut

    with open(config_path, "w") as f:
        json.dump(shortcuts, f, indent=4)
    print(f"快捷键 '{key_name}' 更新为: {new_shortcut}")

CONFIG = load_config()

