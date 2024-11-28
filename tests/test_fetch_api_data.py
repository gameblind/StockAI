import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock


# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from src.data_fetcher.fetch_api_data import fetch_api_data

class TestFetchApiData(unittest.TestCase):
    def setUp(self):
        """
        设置测试环境，包括加载配置文件和模拟 API 数据
        """
        # 模拟配置文件内容
        self.settings = {
            "byapi": {
                "api_url": "http://api.biyingapi.com/",
                "api_key": "5E8ED2F9-381F-44F7-B4E8-F63870456D18",
                "api_data_json_path": "config/api_data_dictionary.json",
            }
        }

        # 模拟 API 数据字典
        self.api_data_dict = [
            {
                "API Key Combined": "rzrq_margin_trading_historical_trends",
                "url_template": "/hsrq/lszs/{stock_code}/{api_key}",
                "API Params": "{\"stock_code\": \"股票代码\", \"api_key\": \"用户授权密钥\"}"
            }
        ]

        # 创建临时目录和文件
        self.test_config_dir = os.path.join(os.getcwd(), "config")
        os.makedirs(self.test_config_dir, exist_ok=True)

        self.settings_path = os.path.join(self.test_config_dir, "settings.json")
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f)

        self.api_data_path = os.path.join(self.test_config_dir, "api_data_dictionary.json")
        with open(self.api_data_path, "w", encoding="utf-8") as f:
            json.dump(self.api_data_dict, f)

    def tearDown(self):
        """
        清理测试环境
        """
        if os.path.exists(self.settings_path):
            os.remove(self.settings_path)
        if os.path.exists(self.api_data_path):
            os.remove(self.api_data_path)
        if os.path.exists(self.test_config_dir):
            os.rmdir(self.test_config_dir)

    @patch("src.data_fetcher.fetch_api_data.requests.get")
    def test_fetch_api_data_success(self, mock_get):
        """
        测试 fetch_api_data 正常情况
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"key": "value"}}
        mock_get.return_value = mock_response

        # 调用 fetch_api_data
        api_key_combined = "rzrq_margin_trading_historical_trends"
        additional_params = {"stock_code": "000001"}
        result = fetch_api_data(api_key_combined, additional_params)

        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertEqual(result["success"], True)
        self.assertIn("data", result)

        # 验证请求 URL
        mock_get.assert_called_once()
        expected_url = "http://api.biyingapi.com/hsrq/lszs/000001/5E8ED2F9-381F-44F7-B4E8-F63870456D18"
        self.assertIn(expected_url, mock_get.call_args[0][0])

    def test_missing_required_params(self):
        """
        测试缺少必要参数的情况
        """
        api_key_combined = "rzrq_margin_trading_historical_trends"
        with self.assertRaises(ValueError) as context:
            fetch_api_data(api_key_combined)
        self.assertIn("缺少必需参数", str(context.exception))

    def test_invalid_api_key_combined(self):
        """
        测试无效的 API Key Combined
        """
        invalid_api_key = "invalid_key"
        with self.assertRaises(ValueError) as context:
            fetch_api_data(invalid_api_key, {"stock_code": "000001"})
        self.assertIn(f"API '{invalid_api_key}' 未找到", str(context.exception))

if __name__ == "__main__":
    unittest.main()