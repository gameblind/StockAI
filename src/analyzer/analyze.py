import pandas as pd
import os
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
class StockAnalyzer:
    def __init__(self):
        pass

    def calculate_technical_indicators(self, historical_data):
        """
        Calculate moving averages and MACD from historical data.
        Args:
            historical_data (list): List of historical price data.
        Returns:
            dict: Calculated indicators.
        """
        df = pd.DataFrame(historical_data)
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        # Calculate MACD
        df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Histogram'] = df['MACD'] - df['Signal']

        return df.tail(1).to_dict(orient="records")[0]

    def analyze_stock(self, stock_data, historical_data):
        """
        Perform a comprehensive analysis on the stock.
        Args:
            stock_data (dict): Current stock data.
            historical_data (list): Historical stock data.
        Returns:
            dict: Analysis result.
        """
        indicators = self.calculate_technical_indicators(historical_data)
        analysis = {
            "current_price": stock_data.get("price"),
            "moving_averages": {
                "MA5": indicators.get("MA5"),
                "MA10": indicators.get("MA10"),
                "MA20": indicators.get("MA20")
            },
            "macd": {
                "MACD": indicators.get("MACD"),
                "Signal": indicators.get("Signal"),
                "Histogram": indicators.get("Histogram")
            },
            "short_term_trend": "Bullish" if indicators.get("MACD") > indicators.get("Signal") else "Bearish"
        }
        return analysis