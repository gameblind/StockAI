import unittest
import os
import json
from src.data_fetcher.fetch_data import (
    fetch_daily_data,
    fetch_60min_data,
    fetch_stock_data,
    clean_and_validate_data,
    save_data_to_file,
    fetch_intraday_data  # 确保 fetch_intraday_data 正确导入
)

class TestFetchData(unittest.TestCase):

    def setUp(self):
        """
        测试前准备工作。
        """
        self.test_symbol = "AAPL"  # 替换为有效股票代码
        self.test_file_path = "tests/output/test_data.json"

    def test_fetch_daily_data(self):
        """
        测试 fetch_daily_data 函数。
        """
        try:
            data = fetch_daily_data(self.test_symbol, days=5)
            self.assertIsInstance(data, list)
            print("Daily Data:", data)
        except ValueError as e:
            print(f"fetch_daily_data 测试警告: {e}")

    def test_fetch_60min_data(self):
        """
        测试 fetch_60min_data 函数。
        """
        data = fetch_60min_data(self.test_symbol)
        self.assertIsInstance(data, list)
        print("60-Min Data:", data)

    def test_fetch_stock_data(self):
        """
        测试 fetch_stock_data 函数。
        """
        try:
            data = fetch_stock_data(self.test_symbol)
            self.assertIn("stock", data)
            print("Stock Data:", data)
        except RuntimeError as e:
            print(f"fetch_stock_data 测试警告: {e}")

    def test_clean_and_validate_data(self):
        """
        测试 clean_and_validate_data 函数。
        """
        raw_data = [
            {"timestamp": "2024-11-22 12:00", "open": "150.5", "close": "152.5", "high": "153", "low": "150", "volume": "1000"},
            {"timestamp": "2024-11-22 14:00", "open": "invalid", "close": "154.0", "high": "155", "low": "152", "volume": "1100"}
        ]
        cleaned_data = clean_and_validate_data(raw_data)
        self.assertEqual(len(cleaned_data), 1)  # 第二条数据应被过滤
        print("Cleaned Data:", cleaned_data)

    def test_save_data_to_file(self):
        """
        测试 save_data_to_file 函数。
        """
        test_data = [{"timestamp": "2024-11-22 12:00", "open": 150.5, "close": 152.5, "high": 153, "low": 150, "volume": 1000}]
        save_data_to_file(test_data, self.test_file_path)
        self.assertTrue(os.path.exists(self.test_file_path))
        with open(self.test_file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(test_data, loaded_data)
        print("Saved Data:", loaded_data)

    def tearDown(self):
        """
        测试完成后清理工作。
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)


if __name__ == "__main__":
    unittest.main()