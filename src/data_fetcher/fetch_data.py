import json
import logging
import os
import requests
import csv

logging.basicConfig(level=logging.INFO)

# 加载 API 配置
def load_api_config():
    settings_path = "config/setting.json"
    try:
        with open(settings_path, "r") as f:
            settings = json.load(f)
        logging.info("API configuration successfully loaded.")
        return {
            "api_key": settings["alphavantage"]["api_key"],
            "base_url": settings["alphavantage"]["api_url"]
        }
    except (FileNotFoundError, KeyError) as e:
        raise ValueError("配置文件错误或缺失，请检查 setting.json 中的 alphavantage 配置。") from e

API_CONFIG = load_api_config()

# 通用的时间序列数据获取函数
def fetch_time_series_data(symbol, interval):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_CONFIG["api_key"]
    }
    response = requests.get(API_CONFIG["base_url"], params=params)
    if response.status_code != 200:
        logging.error(f"API request failed with status code {response.status_code}: {response.text}")
        raise RuntimeError("Failed to fetch data from API.")
    
    response_data = response.json()
    time_series_key = f"Time Series ({interval})"
    
    try:
        time_series = response_data[time_series_key]
        data = [
            {
                "timestamp": timestamp,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            }
            for timestamp, values in time_series.items()
        ]
        logging.info(f"Successfully fetched {interval} data for {symbol}.")
        return data
    except KeyError:
        logging.error(f"API 响应数据解析失败: {response_data}")
        raise ValueError(f"无法获取 {symbol} 的 {interval} 数据，请检查 API 配置或参数。")

# 获取 60 分钟线数据
def fetch_60min_data(symbol):
    return fetch_time_series_data(symbol, "60min")

# 获取实时数据
def fetch_intraday_data(symbol, interval="5min"):
    return fetch_time_series_data(symbol, interval)

# 获取每日历史数据
def fetch_daily_data(symbol, days=5):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_CONFIG["api_key"]
    }
    response = requests.get(API_CONFIG["base_url"], params=params)
    if response.status_code != 200:
        logging.error(f"API request failed with status code {response.status_code}: {response.text}")
        raise RuntimeError("Failed to fetch daily data from API.")

    response_data = response.json()
    try:
        daily_time_series = response_data["Time Series (Daily)"]
        history = [
            {
                "date": date,
                "open": float(values["1. open"]),
                "close": float(values["4. close"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "volume": int(values["5. volume"])
            }
            for date, values in list(daily_time_series.items())[:days]
        ]
        logging.info(f"Successfully fetched daily data for {symbol}.")
        return history
    except KeyError:
        logging.error(f"API 响应数据解析失败: {response_data}")
        raise ValueError(f"无法获取 {symbol} 的每日历史数据，请检查 API 配置或参数。")

# 清洗和验证数据
def clean_and_validate_data(data):
    logging.info("Starting data cleaning and validation.")
    cleaned_data = []
    seen_timestamps = set()

    for idx, entry in enumerate(data):
        try:
            # 验证字段完整性
            required_keys = ["timestamp", "open", "close", "high", "low", "volume"]
            for key in required_keys:
                if key not in entry:
                    raise ValueError(f"Missing required field: {key}")
            
            # 转换类型并验证范围
            entry["open"] = float(entry["open"])
            entry["close"] = float(entry["close"])
            entry["high"] = float(entry["high"])
            entry["low"] = float(entry["low"])
            entry["volume"] = int(entry["volume"])
            if entry["high"] < entry["low"]:
                raise ValueError("High price cannot be lower than low price.")
            if entry["volume"] < 0:
                raise ValueError("Volume cannot be negative.")
            
            # 检查时间戳重复
            if entry["timestamp"] in seen_timestamps:
                raise ValueError("Duplicate timestamp detected.")
            seen_timestamps.add(entry["timestamp"])
            
            cleaned_data.append(entry)
        except (ValueError, KeyError) as e:
            logging.warning(f"Skipping invalid entry at index {idx}: {entry}, Reason: {e}")
    
    logging.info(f"Data cleaning completed. Valid entries: {len(cleaned_data)}")
    return cleaned_data

# 保存数据至文件
def save_data_to_file(data, file_path):
    if not data:
        logging.warning("No data to save. File not created.")
        return
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Data successfully saved to {file_path}.")
    except Exception as e:
        logging.error(f"Failed to save data to {file_path}: {e}")
        raise

# 保存数据至 CSV 文件
def save_data_to_csv(data, file_path):
    if not data:
        logging.warning("No data to save. File not created.")
        return
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Data successfully saved to {file_path}.")
    except Exception as e:
        logging.error(f"Failed to save data to {file_path}: {e}")
        raise

# 获取综合股票数据
def fetch_stock_data(symbol):
    try:
        realtime_data = fetch_intraday_data(symbol, interval="5min")
        history_data = fetch_daily_data(symbol)
        logging.info(f"Fetched stock data for {symbol}.")
        return {
            "stock": {
                "symbol": symbol,
                "realtime": realtime_data,
                "history": history_data
            }
        }
    except Exception as e:
        logging.error(f"Failed to fetch stock data for {symbol}: {e}")
        raise RuntimeError(f"Unable to fetch data for {symbol}.")

# 批量处理股票代码
def fetch_batch_data(symbols):
    results = {}
    success, failure = [], []
    for symbol in symbols:
        try:
            results[symbol] = fetch_stock_data(symbol)
            success.append(symbol)
            logging.info(f"Successfully fetched data for {symbol}.")
        except Exception as e:
            logging.warning(f"Failed to fetch data for {symbol}: {e}")
            failure.append(symbol)
    logging.info(f"Batch fetch completed. Success: {len(success)}, Failure: {len(failure)}.")
    return results