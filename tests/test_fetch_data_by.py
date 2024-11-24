import logging
from datetime import datetime, timedelta
from src.data_fetcher.fetch_data_by import (
    fetch_realtime_data,
    fetch_historical_data,
    clean_and_validate_data,
    save_data_to_file,
    fetch_stock_data,
)

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 测试用的股票代码
test_symbol = "600519"  # 贵州茅台的股票代码
output_file = "tests/output/test_data_by.json"

# 定义测试的时间范围
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")  # 30天前
end_date = datetime.now().strftime("%Y-%m-%d")  # 今天

def test_fetch_realtime_data():
    """
    测试实时数据获取函数
    """
    logging.info("Testing fetch_realtime_data...")
    try:
        data = fetch_realtime_data(test_symbol)
        logging.info(f"Fetched {len(data)} realtime records.")
    except Exception as e:
        logging.error(f"Error fetching realtime data: {e}")

def test_fetch_historical_data():
    """
    测试历史数据获取函数，增加时间段过滤
    """
    logging.info("Testing fetch_historical_data...")
    try:
        # 自定义测试时间段
        start_date = "2024-11-01"  # 开始日期
        end_date = "2024-11-20"    # 截止日期
        period = "dn"              # 日线数据

        logging.info(f"Fetching data for {test_symbol} from {start_date} to {end_date} with period {period}...")
        # 调用 fetch_historical_data，传入时间段和 period 参数
        data = fetch_historical_data(test_symbol, start_date=start_date, end_date=end_date)

        # 根据返回的数据量判断输出内容
        if len(data) > 50:  # 如果数据太多，只显示前50条
            logging.info(f"Fetched {len(data)} records. Showing first 50:\n{data[:50]}")
        else:
            logging.info(f"Fetched {len(data)} records:\n{data}")

    except Exception as e:
        logging.error(f"Error during test_fetch_historical_data: {e}")

def test_clean_and_validate_data():
    """
    测试数据清洗和验证函数
    """
    logging.info("Testing clean_and_validate_data...")
    try:
        raw_data = [
            {"t": "2024-11-22 14:00", "o": "100", "c": "120", "h": "130", "l": "90", "v": "5000"},
            {"t": "2024-11-22 15:00", "o": "invalid", "c": "120", "h": "130", "l": "90", "v": "5000"},
        ]
        cleaned_data = clean_and_validate_data(raw_data)
        logging.info(f"Cleaned Data: {cleaned_data}")
    except Exception as e:
        logging.error(f"Error in data cleaning: {e}")

def test_save_data_to_file():
    """
    测试保存数据至文件函数
    """
    logging.info("Testing save_data_to_file...")
    try:
        test_data = [
            {"t": "2024-11-22 14:00", "o": 100, "c": 120, "h": 130, "l": 90, "v": 5000},
        ]
        save_data_to_file(test_data, output_file)
        logging.info(f"Data saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving data to file: {e}")

def test_fetch_combined_data():
    """
    测试综合数据获取函数
    """
    logging.info("Testing fetch_stock_data...")
    try:
        data = fetch_stock_data(test_symbol)
        if len(data) > 50:  # 如果数据太多，只显示前50条
            logging.info(f"Fetched {len(data)} records. Showing first 50:\n{data[:50]}")
        else:
            logging.info(f"Fetched data:\n{data}")
    except Exception as e:
        logging.error(f"Error fetching combined stock data: {e}")

if __name__ == "__main__":
    # 按顺序运行测试
    test_fetch_realtime_data()
    test_fetch_historical_data()
    test_clean_and_validate_data()
    test_save_data_to_file()
    test_fetch_combined_data()