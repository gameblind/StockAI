import os
import sys
import unittest
import json

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from src.data_fetcher.by_api_manager import ByApiManager  # 确保路径正确

class TestByApiManager(unittest.TestCase):
    def setUp(self):
        """
        初始化测试环境
        """
        self.settings = {
            "byapi": {
                "api_url": "http://api.biyingapi.com/",
                "api_key": "5E8ED2F9-381F-44F7-B4E8-F63870456D18",  # 确保 api_key 存在
                "api_data_json_path": "config/api_data_dictionary.json",
                "fields_data_json_path": "config/fields_data_dictionary.json",
            }
        }
        self.api_manager = ByApiManager(self.settings)

    def test_load_api_data(self):
        """
        测试是否能够正确加载 API 数据字典
        """
        api_data = self.api_manager.api_data
        self.assertTrue(isinstance(api_data, dict))
        self.assertIn("rzrq_margin_trading_historical_trends", api_data)

    def test_load_fields_data(self):
        """
        测试是否能够正确加载字段数据字典
        """
        fields_data = self.api_manager.fields_data
        self.assertTrue(isinstance(fields_data, list))
        self.assertGreater(len(fields_data), 0)

    def test_fetch_api_data(self):
        """
        测试 fetch_api_data 方法
        """
        api_key_combined = "rzrq_margin_trading_historical_trends"  # 确保此键值正确
        additional_params = {"stock_code": "000001", "api_key": self.settings["byapi"]["api_key"]}

        try:
            result = self.api_manager.fetch_api_data(api_key_combined, additional_params)
            self.assertIsInstance(result, dict)  # 确保返回值是字典
        except Exception as e:
            self.fail(f"fetch_api_data 测试失败: {e}")

    def test_get_fields_by_api_key(self):
        """
        测试 get_fields_by_api_key 方法
        """
        api_key_combined = "rzrq_margin_trading_historical_trends"
        fields = self.api_manager.get_fields_by_api_key(api_key_combined)
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)
        self.assertEqual(fields[0]["API Key Combined"], api_key_combined)

if __name__ == "__main__":
    unittest.main()