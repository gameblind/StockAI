import os
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
import unittest
from src.data_fetcher.fetch_api_data import fetch_api_data

class TestFetchAPIData(unittest.TestCase):
    def test_margin_trading_target_stocks(self):
        """测试融资融券标的股接口"""
        try:
            result = fetch_api_data(
                api_key_combined="rzrq_margin_trading_target_stocks",
                additional_params={}
            )
            print("[INFO] 融资融券标的股接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_margin_trading_historical_trends(self):
        """测试融资融券历史走势接口"""
        try:
            result = fetch_api_data(
                api_key_combined="rzrq_margin_trading_historical_trends",
                additional_params={"stock_code": "000001"}
            )
            print("[INFO] 融资融券历史走势接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_historical_intraday_trading(self):
        """测试历史分时交易接口"""
        try:
            result = fetch_api_data(
                api_key_combined="lssj_historical_intraday_trading",
                additional_params={"stock_code": "000001", "time_frame": "15m"}
            )
            print("[INFO] 历史分时交易接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_historical_intraday_macd(self):
        """测试历史分时MACD接口"""
        try:
            result = fetch_api_data(
                api_key_combined="lssj_historical_intraday_macd",
                additional_params={"stock_code": "000001", "time_frame": "15m"}
            )
            print("[INFO] 历史分时MACD接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_institutional_holdings_summary(self):
        """测试机构持股汇总接口"""
        try:
            result = fetch_api_data(
                api_key_combined="jgcg_institutional_holdings_summary",
                additional_params={"year": "2023", "quarter": "1"}
            )
            print("[INFO] 机构持股汇总接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_heavy_fund_positions(self):
        """测试基金重仓接口"""
        try:
            result = fetch_api_data(
                api_key_combined="jgcg_heavy_fund_positions",
                additional_params={"year": "2023", "quarter": "1"}
            )
            print("[INFO] 基金重仓接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_social_security_heavy_positions(self):
        """测试社保重仓接口"""
        try:
            result = fetch_api_data(
                api_key_combined="jgcg_social_security_heavy_positions",
                additional_params={"year": "2023", "quarter": "1"}
            )
            print("[INFO] 社保重仓接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

    def test_qfii_heavy_positions(self):
        """测试QFII重仓股接口"""
        try:
            result = fetch_api_data(
                api_key_combined="jgcg_qfii_heavy_positions",
                additional_params={"year": "2023", "quarter": "1"}
            )
            print("[INFO] QFII重仓股接口返回数据:", result)
        except Exception as e:
            self.fail(f"测试失败: {e}")

if __name__ == "__main__":
    print("[INFO] 测试开始...")
    unittest.main()