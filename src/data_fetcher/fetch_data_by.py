import json
import logging
import os
import requests
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

logging.basicConfig(level=logging.INFO)

# 加载 API 配置
def load_api_config():
    settings_path = "config/settings.json"
    try:
        with open(settings_path, "r") as f:
            settings = json.load(f)
        return {
            "api_key": settings["byapi"]["api_key"],
            "base_url": settings["byapi"]["api_url"]
        }
    except (FileNotFoundError, KeyError) as e:
        raise ValueError("配置文件错误或缺失，请检查 setting.json 中的 byapi 配置。") from e

API_CONFIG = load_api_config()

# 获取沪深股票列表
def fetch_stock_list():
    url = f"{API_CONFIG['base_url']}hslt/list/{API_CONFIG['api_key']}"
    response = requests.get(url)
    response_data = response.json()
    if isinstance(response_data, list):
        return response_data
    else:
        logging.error(f"API 响应数据解析失败: {response_data}")
        raise ValueError("无法获取股票列表，请检查 API 配置或参数。")

# 获取实时交易数据
def fetch_realtime_data(symbol):
    """
    获取股票的实时交易数据
    """
    url = f"{API_CONFIG['base_url']}hsrl/ssjy/{symbol}/{API_CONFIG['api_key']}"
    response = requests.get(url)
    response_data = response.json()

    try:
        # 提取并格式化返回数据
        realtime_data = {
            "open": float(response_data["o"]),  # 开盘价
            "high": float(response_data["h"]),  # 最高价
            "low": float(response_data["l"]),  # 最低价
            "latest_price": float(response_data["p"]),  # 最新价格
            "volume": int(response_data["v"]),  # 成交量
            "timestamp": response_data["t"],  # 时间戳
            "change_amount": float(response_data["ud"]),  # 涨跌额
            "change_percent": float(response_data["pc"]),  # 涨跌幅
        }
        return realtime_data
    except KeyError as e:
        logging.error(f"API 响应数据解析失败: {response_data}")
        raise ValueError(f"无法获取 {symbol} 的实时交易数据，请检查 API 配置或参数。") from e
    
# 获取历史交易数据
def fetch_historical_data(symbol, start_date=None, end_date=None):
    """
    获取历史交易数据 (历史成交分布)，支持时间范围过滤
    Args:
        symbol (str): 股票代码，例如 '000001'
        start_date (str): 开始日期（格式 'YYYY-MM-DD'），默认最近10天
        end_date (str): 截止日期（格式 'YYYY-MM-DD'），默认今天
    Returns:
        list: 历史成交分布数据列表
    """
    from datetime import datetime, timedelta

    # 确保 symbol 格式正确（去除 sh、sz 前缀，只保留纯数字代码）
    symbol = symbol.replace("sh", "").replace("sz", "")

    # 默认获取最近10天的数据
    if not start_date:
        start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # 构建 API 请求 URL，假设 API 支持时间参数
    url = f"{API_CONFIG['base_url']}hsmy/lscj/{symbol}/{API_CONFIG['api_key']}"
    logging.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}...")

    try:
        # 模拟 API 调用 (替换为真实 API 请求逻辑)
        response = requests.get(url)
        response.raise_for_status()
        raw_data = response.json()

        # 过滤数据
        filtered_data = [
            record for record in raw_data
            if start_date <= record['t'] <= end_date
        ]

        logging.info(f"Fetched {len(filtered_data)} records for the specified date range.")
        return filtered_data
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        return []
    
# 清洗和验证数据
def clean_and_validate_data(data):
    logging.info("开始数据清洗和验证。")
    cleaned_data = []
    seen_timestamps = set()

    for entry in data:
        try:
            # 验证字段完整性
            required_keys = ["t", "o", "c", "h", "l", "v"]
            for key in required_keys:
                if key not in entry:
                    raise ValueError(f"缺少必要字段: {key}")
            
            # 转换类型并验证范围
            entry["o"] = float(entry["o"])
            entry["c"] = float(entry["c"])
            entry["h"] = float(entry["h"])
            entry["l"] = float(entry["l"])
            entry["v"] = int(entry["v"])
            if entry["h"] < entry["l"]:
                raise ValueError("最高价不能低于最低价。")
            if entry["v"] < 0:
                raise ValueError("成交量不能为负。")
            
            # 检查时间戳重复
            if entry["t"] in seen_timestamps:
                raise ValueError("检测到重复的时间戳。")
            seen_timestamps.add(entry["t"])
            
            cleaned_data.append(entry)
        except (ValueError, KeyError) as e:
            logging.warning(f"跳过无效条目: {entry}, 原因: {e}")
    
    logging.info(f"数据清洗完成。有效条目数: {len(cleaned_data)}")
    return cleaned_data

# 保存数据至文件
def save_data_to_file(data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"数据成功保存至 {file_path}")
    except Exception as e:
        logging.error(f"保存数据至 {file_path} 失败: {e}")
        raise

# 获取综合股票数据
def fetch_stock_data(symbol):
    """
    获取股票的实时和历史数据。
    """
    try:
        # 实时数据
        realtime_data = fetch_realtime_data(symbol)
        # 历史数据
        history_data = fetch_historical_data(symbol)
        return {
            "stock": {
                "symbol": symbol,
                "realtime": realtime_data,
                "history": history_data
            }
        }
    except Exception as e:
        logging.error(f"获取 {symbol} 数据时出错: {e}")
        raise RuntimeError(f"无法获取 {symbol} 的股票数据。")

# 保存数据到 CSV 文件
def save_data_to_csv(data, file_path):
    """
    将数据保存为 CSV 文件。
    """
    import csv
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"数据成功保存至 {file_path}")
    except Exception as e:
        logging.error(f"保存数据至 {file_path} 失败: {e}")
        raise

# 批量处理股票代码
def fetch_batch_data(symbols):
    """
    批量获取股票数据。
    Args:
        symbols (list): 股票代码列表。
    Returns:
        dict: 每个股票的实时和历史数据。
    """
    results = {}
    for symbol in symbols:
        try:
            results[symbol] = fetch_stock_data(symbol)
            logging.info(f"成功获取 {symbol} 的数据。")
        except Exception as e:
            logging.warning(f"获取 {symbol} 的数据失败: {e}")
    return results
def handle_exception(e, context=""):
    """
    统一异常处理函数。
    
    Args:
        e (Exception): 捕获的异常对象。
        context (str): 出错的上下文信息，例如函数名或模块名。
    
    Raises:
        RuntimeError: 包装后的运行时异常，附带详细的上下文信息。
    """
    logging.error(f"Error occurred in {context}: {e}")
    raise RuntimeError(f"An error occurred in {context}. Details: {str(e)}") from e
