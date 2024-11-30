import os
import sys
import json
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


def get_realtime_data(stock_code, api_key_combined):
    """
    获取实时盯盘数据的通用函数。

    :param stock_code: str, 股票代码
    :param api_key_combined: str, API 字典中对应的 API Key
    :return: dict, 返回的 API 数据
    """
    try:
        data = fetch_api_data(api_key_combined, {"stock_code": stock_code})
        logging.info(f"成功获取实时数据: {api_key_combined} -> {stock_code}")
        return data
    except Exception as e:
        logging.error(f"获取实时数据失败: {api_key_combined} -> {stock_code}, 错误: {e}")
        return {}


def map_field_names(api_key_combined, data):
    """
    将数据字段名替换为中文字段名。

    :param api_key_combined: str, API Key Combined
    :param data: list[dict] 或 dict, API 返回的数据
    :return: list[dict] 或 dict, 替换后的数据
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
            raise ValueError(f"未找到 API Key Combined 为 '{api_key_combined}' 的字段映射")

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
        logging.error(f"字段名映射失败: {e}")
        return data


def save_realtime_data_to_txt(data, file_path, api_key_combined):
    """
    保存实时盯盘数据到 TXT 文件，并将字段名替换为中文。

    :param data: dict, API 返回的原始数据
    :param file_path: str, TXT 文件路径
    :param api_key_combined: str, API Key Combined
    """
    try:
        mapped_data = map_field_names(api_key_combined, data)

        # 确保文件夹路径存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 追加写入 TXT 文件
        with open(file_path, "a", encoding="utf-8") as txt_file:
            txt_file.write(f"==== 数据来源: {api_key_combined} ====\n")
            txt_file.write(json.dumps(mapped_data, ensure_ascii=False, indent=4))
            txt_file.write("\n\n")  # 数据项间留空行

        logging.info(f"实时数据已追加保存到: {file_path}")
    except Exception as e:
        logging.error(f"保存实时数据失败: {file_path}, 错误: {e}")


def analyze_realtime_data(txt_file_path):
    """
    分析实时股票数据并生成提醒信号。

    :param txt_file_path: str, 包含股票数据的 TXT 文件路径
    :return: dict, 分析结果
    """
    try:
        with open(txt_file_path, "r", encoding="utf-8") as txt_file:
            file_content = txt_file.read()

        prompt_text = f"""
        以下是实时盯盘数据，包括实时交易数据、买卖五档盘口、逐笔交易、大单交易、分时成交和分价成交占比。
        请分析这些数据，并按照以下格式输出：
        - 当前走势判断（上涨、下跌、横盘、震荡）及概率：
        - 主力资金动向分析：
        - 短线操作建议：
        数据如下：
        {file_content}
        """

        model_name = "gpt-4-all"
        result = submit_request_to_api(model_name, prompt_text, "", CONFIG)

        if not result or "choices" not in result or not result["choices"]:
            raise ValueError("大模型未返回有效结果")

        content = result["choices"][0]["message"]["content"]
        logging.info(f"大模型分析结果:\n{content}")

        output_folder = "data/realtime_analysis_results"
        os.makedirs(output_folder, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"analysis_{timestamp}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"实时分析结果已保存到: {output_file}")

        return {"success": True, "analysis": content}

    except Exception as e:
        logging.error(f"实时数据分析失败: {e}")
        return {"success": False, "error": str(e)}


def notify_user(alerts):
    """
    通知用户分析结果。

    :param alerts: list[str], 提醒信息
    """
    for alert in alerts:
        logging.info(f"[提醒] {alert}")


def stock_realtime_monitor(stock_code):
    """
    实时股票盯盘主函数。

    :param stock_code: str, 股票代码
    """
    logging.info(f"开始实时盯盘: 股票代码={stock_code}")

    api_list = {
        "ssjy_real-time_trading_data_interface": "实时交易数据",
        "ssjy_five-tier_market_order_book": "买卖五档盘口",
        "ssjy_intraday_transactions": "当天逐笔交易",
        "ssjy_intraday_time-sharing_transactions": "当天分时成交",
        "ssjy_intraday_price-by-price_turnover": "当天分价成交占比",
        "ssjy_intraday_large_single_transactions": "当天逐笔大单交易"
    }

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_file_path = f"data/realtime_monitor/{stock_code}_realtime_{timestamp}.txt"

    for api_key_combined, description in api_list.items():
        try:
            data = get_realtime_data(stock_code, api_key_combined)
            save_realtime_data_to_txt(data, txt_file_path, api_key_combined)
        except Exception as e:
            logging.error(f"{description} 数据处理失败: {e}")

    analysis_results = analyze_realtime_data(txt_file_path)
    if analysis_results["success"]:
        logging.info(f"分析结果:\n{analysis_results['analysis']}")
        notify_user(["实时盯盘分析完成！请检查分析结果文件。"])
    else:
        logging.error(f"分析失败: {analysis_results['error']}")


if __name__ == "__main__":
    stock_realtime_monitor("300624")