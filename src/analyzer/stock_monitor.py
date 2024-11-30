import os
import sys
import json
import pandas as pd
import logging
import datetime
from src.data_fetcher.fetch_api_data import fetch_api_data
from src.llm.api_request import submit_request_to_api, CONFIG


# 动态添加项目根目录到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 配置日志
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# 数据获取模块
def get_stock_data(stock_code, date, api_key_combined, additional_params=None):
    """
    获取股票数据的通用函数。

    :param stock_code: str, 股票代码
    :param date: str, 日期 (YYYY-MM-DD)
    :param api_key_combined: str, API 字典中对应的 API Key
    :param additional_params: dict, 可选的额外参数
    :return: dict, 返回的 API 数据
    """
    try:
        if additional_params is None:
            additional_params = {}
        additional_params.update({"stock_code": stock_code, "date": date})
        data = fetch_api_data(api_key_combined, additional_params)
        logging.info(f"成功获取数据: {api_key_combined} -> {stock_code}")
        return data
    except Exception as e:
        logging.error(f"获取数据失败: {api_key_combined} -> {stock_code}, 错误: {e}")
        return {}


def map_field_names(api_key_combined, data):
    """
    根据API字段映射将field_name替换为field_description.

    :param api_key_combined: str, 对应的API Key Combined
    :param data: list[dict], API返回的数据
    :return: 替换字段名后的数据
    """
    try:
        fields_map = {}
        with open("config/api_fields_dictionary.json", "r", encoding="utf-8") as f:
            api_data = json.load(f)
        
        for api in api_data:
            if api["API Key Combined"] == api_key_combined:
                fields_map = {field["field_name"]: field["field_description"] for field in api["fields"]}
                break

        if not fields_map:
            raise ValueError(f"未找到API Key Combined为'{api_key_combined}'的字段映射")

        if isinstance(data, list):
            mapped_data = [
                {fields_map.get(key, key): value for key, value in item.items()}
                for item in data
            ]
        elif isinstance(data, dict):
            mapped_data = {fields_map.get(key, key): value for key, value in data.items()}
        else:
            raise ValueError("不支持的数据格式")

        return mapped_data
    except Exception as e:
        logging.error(f"字段名替换失败: {e}")
        return data

def save_data_to_txt(data, file_path, api_key_combined):
    """
    追加保存映射字段名后的数据到 TXT 文件，并将字段名替换为中文。

    :param data: list[dict] 或 dict, API 返回的原始数据
    :param file_path: str, TXT 文件路径
    :param api_key_combined: str, API Key Combined
    """
    try:
        # 调用字段名映射函数，替换字段为中文
        mapped_data = map_field_names(api_key_combined, data)

        if isinstance(mapped_data, dict):
            mapped_data = [mapped_data]
        if not isinstance(mapped_data, list):
            raise ValueError("数据格式错误，无法保存为 TXT")

        # 确保文件夹路径存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 追加写入 TXT 文件
        with open(file_path, "a", encoding="utf-8") as txt_file:
            txt_file.write(f"==== 数据来源: {api_key_combined} ====\n")
            for item in mapped_data:
                txt_file.write(json.dumps(item, ensure_ascii=False, indent=4))
                txt_file.write("\n\n")  # 数据项间留空行

        logging.info(f"数据已追加保存到: {file_path}")
    except Exception as e:
        logging.error(f"保存数据失败: {file_path}, 错误: {e}")

def save_data_to_csv(data, file_path, api_key_combined):
    """
    保存数据到 CSV 文件，并将字段名替换为中文。

    :param data: list[dict], 数据列表
    :param file_path: str, CSV 文件路径
    :param api_key_combined: str, API Key Combined
    """
    try:
        mapped_data = map_field_names(api_key_combined, data)

        if isinstance(mapped_data, dict):
            mapped_data = [mapped_data]
        if not isinstance(mapped_data, list):
            raise ValueError("数据格式错误，无法保存为 CSV")

        df = pd.DataFrame(mapped_data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False, encoding="utf-8")
        logging.info(f"数据已保存到: {file_path}")
    except Exception as e:
        logging.error(f"保存数据失败: {file_path}, 错误: {e}")


def analyze_data(txt_file_path, output_folder="data/analysis_results"):
    """
    分析股票数据并生成提醒信号。
    
    :param txt_file_path: str, 包含股票数据的 TXT 文件路径
    :param output_folder: str, 保存分析结果的文件夹路径
    :return: dict, 分析结果
    """
    try:
        # 读取 TXT 文件内容作为大模型输入
        with open(txt_file_path, "r", encoding="utf-8") as txt_file:
            file_content = txt_file.read()

        # 提示词优化
        prompt_text = f"""
        请结合近期的数据分析以下股票数据并按照以下格式输出：
        - 短期量价走势判断及概率：
        - 历史股价走势分析及中长期走势判断及概率：
        - 资金流向分析：
        - 技术指标（MACD、KDJ等）分析：
        - 压力位、支撑位及操作建议：
        数据如下：
        {file_content}
        """
        
        # 调用大模型
        model_name = "gpt-4-all"  # 替换为实际使用的模型名称
        settings = CONFIG  # 从配置加载
        result = submit_request_to_api(model_name, prompt_text, "", settings)
        
        # 验证模型返回内容
        if not result or "choices" not in result or not result["choices"]:
            raise ValueError("大模型未返回有效结果")

        # 提取模型生成的内容
        content = result["choices"][0]["message"]["content"]
        logging.info(f"大模型分析结果:\n{content}")

        # 保存分析结果到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"analysis_{timestamp}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        logging.info(f"分析结果已保存到: {output_file}")

        # 返回结果
        return {"alerts": ["分析完成，请检查分析文件"], "raw_result": content}

    except Exception as e:
        logging.error(f"分析数据失败: {e}")
        return {"alerts": ["分析失败"], "raw_result": None}

def notify_user(alerts):
    """
    通知用户分析结果。

    :param alerts: list[str], 提醒信息
    """
    for alert in alerts:
        logging.info(f"[提醒] {alert}")
        

def monitor_stock(stock_code, date):
    """
    股票盯盘主函数。

    :param stock_code: str, 股票代码
    :param date: str, 日期 (YYYY-MM-DD)
    """
    logging.info(f"开始盯盘: 股票代码={stock_code}, 日期={date}")

    api_list = {
        "realtime_trading": "ssjy_real-time_trading_data_interface",
        "histrical_trading": "lssj_historical_intraday_trading",
        "funds_flow": "ssjy_intraday_large_single_transactions",
        "intraday_kdj": "lssj_historical_intraday_kdj(9,3,3)",
        "intraday_macd": "lssj_historical_intraday_macd",
        "market_order_book": "ssjy_five-tier_market_order_book",
    }

    all_data = {}

    for key, api_key_combined in api_list.items():
        additional_params = None
        if "kdj" in key or "macd" or "histrical" in key:
            additional_params = {"time_frame": "dn", "index_code": key.split("_")[-1].upper()}
        all_data[key] = get_stock_data(stock_code, date, api_key_combined, additional_params)

    # 使用 datetime 模块生成时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_file_path = f"data/{stock_code}_{timestamp}_summary.txt"

    for key, data in all_data.items():
        api_key_combined = api_list[key]
        try:
            save_data_to_csv(data, f"data/{stock_code}_{key}.csv", api_key_combined=api_key_combined)
            save_data_to_txt(data, txt_file_path, api_key_combined=api_key_combined)
        except Exception as e:
            logging.error(f"处理数据失败: {key}, 错误: {e}")

    analysis_results = analyze_data(txt_file_path)


    if analysis_results["success"]:
        logging.info(f"分析结果:\n{analysis_results['analysis']}")
        notify_user(analysis_results["alerts"])
    else:
        logging.error(f"分析失败: {analysis_results['error']}")

if __name__ == "__main__":
    monitor_stock("300624", "2024-11-29")