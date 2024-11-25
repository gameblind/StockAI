import json
import requests
import os
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def fetch_api_data(api_key_combined, additional_params=None, **kwargs):
    """
    动态获取 API 数据（从配置文件读取 api_key）。

    :param api_key_combined: str, 唯一主键 (Category Code + "_" + API Code)
    :param additional_params: dict, 动态参数（如 stock_code 等，不包括 api_key）
    :param kwargs: dict, 其他可选参数
    :return: dict or list, 返回 API 请求的结果
    """
    try:
        # 获取项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

        # 加载配置文件
        config_path = os.path.join(project_root, "config", "settings.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件未找到: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        # 从配置文件中获取 api_key
        api_key = settings.get("byapi", {}).get("api_key")
        if not api_key:
            raise ValueError("配置文件中未找到有效的 api_key")

        # 加载 API 数据字典
        api_data_path = os.path.join(project_root, settings["byapi"]["api_data_json_path"])
        if not os.path.exists(api_data_path):
            raise FileNotFoundError(f"API 数据字典未找到: {api_data_path}")
        with open(api_data_path, "r", encoding="utf-8") as f:
            api_data_dict = json.load(f)

        # 查找指定 API Key Combined
        api_info = next(
            (item for item in api_data_dict if item.get("API Key Combined") == api_key_combined),
            None
        )
        if not api_info:
            raise ValueError(f"API '{api_key_combined}' 未找到")
        # 提取 URL 模板和必需参数
        url_template = api_info.get("url_template", "")
        required_params = json.loads(api_info.get("API Params", "{}"))

        # 检查必需参数
        if additional_params is None:
            additional_params = {}

        # 如果 'api_key' 是必需参数，且在 settings 文件中提供，则从校验中移除
        if "api_key" in required_params and "api_key" in settings["byapi"]:
            del required_params["api_key"]

        # 校验缺失的必需参数
        missing_params = [key for key in required_params if key not in additional_params]
        if missing_params:
            raise ValueError(f"缺少必需参数: {missing_params}")

        # 格式化 URL
        formatted_params = {**additional_params, "api_key": settings["byapi"]["api_key"]}
        api_url = url_template.format(**formatted_params)
        full_url = f"{settings['byapi']['api_url'].rstrip('/')}/{api_url.lstrip('/')}"

        print(f"[DEBUG] 拼接后的完整 URL: {full_url}")

        # 发起请求
        response = requests.get(full_url, params=kwargs)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        raise RuntimeError(f"[ERROR] 获取 API 数据失败: {e}")