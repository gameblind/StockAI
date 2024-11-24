import os
import json

class ConfigManager:
    def __init__(self, config_path="config/setting.json"):  # 更新文件名为 settings.json
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        加载主配置文件
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件未找到: {self.config_path}")
        with open(self.config_path, "r") as f:
            return json.load(f)

    def get(self, key, default=None):
        """
        获取配置值
        Args:
            key (str): 配置的键
            default: 如果键不存在，返回的默认值
        Returns:
            配置的值
        """
        return self.config.get(key, default)

    def update(self, key, value):
        """
        更新配置并写入文件
        Args:
            key (str): 要更新的键
            value: 新值
        """
        self.config[key] = value
        self.save_config()

    def save_config(self):
        """
        保存配置到文件
        """
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        print(f"配置文件已更新: {self.config_path}")

    def update_shortcut(self, key_name, new_shortcut):
        """
        更新快捷键配置
        Args:
            key_name (str): 要修改的快捷键名称（如 'screenshot'）
            new_shortcut (str): 新的快捷键组合（如 'ctrl+shift+s'）
        """
        shortcuts = self.config.get("shortcuts", {})
        shortcuts[key_name] = new_shortcut
        self.config["shortcuts"] = shortcuts
        self.save_config()
        print(f"快捷键 '{key_name}' 更新为: {new_shortcut}")


# 初始化全局配置
CONFIG_MANAGER = ConfigManager()