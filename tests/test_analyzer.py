import unittest
from src.analyzer.analyze import StockAnalyzer

class TestStockAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = StockAnalyzer()
        self.historical_data = [
            {"date": "2024-11-01", "close": 100},
            {"date": "2024-11-02", "close": 102},
            {"date": "2024-11-03", "close": 104},
            {"date": "2024-11-04", "close": 106},
            {"date": "2024-11-05", "close": 108},
        ]

    def test_calculate_technical_indicators(self):
        indicators = self.analyzer.calculate_technical_indicators(self.historical_data)
        self.assertIn("MA5", indicators)
        self.assertIn("MACD", indicators)
        self.assertIn("Signal", indicators)

    def test_analyze_stock(self):
        stock_data = {"price": 108}
        analysis = self.analyzer.analyze_stock(stock_data, self.historical_data)
        self.assertIn("current_price", analysis)
        self.assertIn("moving_averages", analysis)
        self.assertIn("macd", analysis)
        self.assertIn("short_term_trend", analysis)

if __name__ == "__main__":
    unittest.main()