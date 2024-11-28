import os
import sys
import json
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from matplotlib import font_manager, rcParams
from datetime import datetime
from math import pi

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_fetcher.fetch_api_data import fetch_api_data



def fetch_stock_data(stock_code):
    """
    Fetches key stock data for a given stock code.
    """
    try:
        print(f"[INFO] 开始获取股票 {stock_code} 的数据")
        return {
            "实时数据": fetch_api_data(
                api_key_combined="ssjy_real-time_trading_data_interface",
                additional_params={"stock_code": stock_code}
            ),
            "历史分时交易数据": fetch_api_data(
                api_key_combined="lssj_historical_intraday_trading",
                additional_params={"stock_code": stock_code, "time_frame": "15m"}
            ),
            "历史MACD指标": fetch_api_data(
                api_key_combined="lssj_historical_intraday_macd",
                additional_params={"stock_code": stock_code, "time_frame": "15m"}
            ),
            "财务指标数据": fetch_api_data(
                api_key_combined="gsxq_financial_indicators",
                additional_params={"stock_code": stock_code}
            ),
            "十大股东数据": fetch_api_data(
                api_key_combined="gsxq_top_ten_shareholders",
                additional_params={"stock_code": stock_code}
            ),
            "基金重仓数据": fetch_api_data(
                api_key_combined="jgcg_heavy_fund_positions",
                additional_params={"year": str(datetime.now().year), "quarter": "1"}
            ),
            "概念板块数据": fetch_api_data(
                api_key_combined="bkzj_concept_sectors",
                additional_params={}
            )
        }
    except Exception as e:
        print(f"[ERROR] 数据获取失败: {e}")
        return None


def save_data_by_api(data):
    """
    Saves data by API into separate files.
    """
    for api_name, api_data in data.items():
        filename = f"{api_name}.json"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(api_data, file, indent=4, ensure_ascii=False)
            print(f"[INFO] 数据已保存至文件: {filename}")
        except Exception as e:
            print(f"[ERROR] 保存文件 {filename} 失败: {e}")


def set_chinese_font():
    """
    Sets a font that supports Chinese for Matplotlib.
    """
    # 手动指定字体路径（宋体）
    font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
    if not os.path.exists(font_path):
        raise RuntimeError("未找到指定的字体文件！")
    return font_manager.FontProperties(fname=font_path)

def generate_charts(data):
    """
    Generates charts based on each API's data.
    """
    # 设置字体
    font_prop = set_chinese_font()
    rcParams['font.family'] = font_prop.get_name()  # 全局设置字体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 实时数据图表（改为折线图）
    if "实时数据" in data:
        realtime_data = data["实时数据"]
        if all(key in realtime_data for key in ["o", "h", "l", "p"]):
            prices = [realtime_data["o"], realtime_data["h"], realtime_data["l"], realtime_data["p"]]
            labels = ["开盘价", "最高价", "最低价", "收盘价"]
            plt.figure(figsize=(8, 6))
            plt.plot(labels, prices, marker='o', color='blue', linestyle='-', label="价格")
            plt.title("实时价格数据", fontproperties=font_prop)
            plt.ylabel("价格", fontproperties=font_prop)
            plt.grid(True)
            plt.legend(prop=font_prop)
            plt.savefig("实时价格折线图.png")
            plt.close()
            print("[INFO] 实时价格折线图已生成：实时价格折线图.png")

    # 历史分时交易数据图表（K线图 + 成交量柱状图）
    if "历史分时交易数据" in data:
        historical_data = data["历史分时交易数据"]
        if isinstance(historical_data, list) and len(historical_data) > 0:
            df = pd.DataFrame(historical_data)
            if all(col in df.columns for col in ['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量']):
                df['时间'] = pd.to_datetime(df['时间'])
                df.set_index('时间', inplace=True)

                # 生成K线图
                df.rename(columns={
                    '开盘价': 'Open',
                    '最高价': 'High',
                    '最低价': 'Low',
                    '收盘价': 'Close',
                    '成交量': 'Volume'
                }, inplace=True)
                mpf.plot(
                    df,
                    type='candle',
                    style='charles',
                    title="历史K线图",
                    ylabel='价格',
                    ylabel_lower='成交量',
                    volume=True,
                    savefig="历史K线图.png"
                )
                print("[INFO] K线图已生成：历史K线图.png")

                # 生成成交量柱状图
                plt.figure(figsize=(12, 6))
                plt.bar(df.index, df['Volume'], color='blue', alpha=0.6)
                plt.title("历史分时交易成交量", fontproperties=font_prop)
                plt.ylabel("成交量", fontproperties=font_prop)
                plt.xlabel("时间", fontproperties=font_prop)
                plt.grid(True)
                plt.savefig("历史分时交易成交量图.png")
                plt.close()
                print("[INFO] 成交量图已生成：历史分时交易成交量图.png")

    # 历史MACD指标图表
    if "历史MACD指标" in data:
        macd_data = data["历史MACD指标"]
        if isinstance(macd_data, list) and len(macd_data) > 0:
            df = pd.DataFrame(macd_data)
            if all(col in df.columns for col in ['时间', 'DIF', 'DEA', 'MACD']):
                df['时间'] = pd.to_datetime(df['时间'])
                df.set_index('时间', inplace=True)

                # 生成MACD图
                plt.figure(figsize=(12, 6))
                plt.plot(df.index, df['DIF'], label="DIF", color='blue')
                plt.plot(df.index, df['DEA'], label="DEA", color='red')
                plt.bar(df.index, df['MACD'], color=['green' if m > 0 else 'red' for m in df['MACD']])
                plt.title("MACD 指标", fontproperties=font_prop)
                plt.xlabel("时间", fontproperties=font_prop)
                plt.ylabel("值", fontproperties=font_prop)
                plt.legend(prop=font_prop)
                plt.grid(True)
                plt.savefig("MACD指标图.png")
                plt.close()
                print("[INFO] MACD 图已生成：MACD指标图.png")

    # 财务指标雷达图
    if "财务指标数据" in data:
        financial_data = data["财务指标数据"]
        if isinstance(financial_data, list) and len(financial_data) > 0:
            df = pd.DataFrame(financial_data)
            categories = df['指标名称']
            values = df['指标值']

            # 雷达图数据准备
            values = list(values) + [values[0]]  # 闭合雷达图
            angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
            angles += angles[:1]

            # 绘制雷达图
            plt.figure(figsize=(8, 8))
            ax = plt.subplot(111, polar=True)
            plt.xticks(angles[:-1], categories, fontproperties=font_prop)
            ax.plot(angles, values, linewidth=2, linestyle='solid')
            ax.fill(angles, values, alpha=0.4)
            plt.title("财务指标雷达图", fontproperties=font_prop)
            plt.savefig("财务指标雷达图.png")
            plt.close()
            print("[INFO] 财务指标雷达图已生成：财务指标雷达图.png")

    # 基金重仓数据饼图
    if "基金重仓数据" in data:
        fund_data = data["基金重仓数据"]
        if isinstance(fund_data, list) and len(fund_data) > 0:
            df = pd.DataFrame(fund_data)
            labels = df['基金名称']
            sizes = df['持仓比例']

            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font_prop})
            plt.title("基金持仓分布", fontproperties=font_prop)
            plt.savefig("基金持仓分布图.png")
            plt.close()
            print("[INFO] 基金持仓分布图已生成：基金持仓分布图.png")

    # 概念板块涨跌幅条形图
    if "概念板块数据" in data:
        sector_data = data["概念板块数据"]
        if isinstance(sector_data, list) and len(sector_data) > 0:
            df = pd.DataFrame(sector_data)
            plt.figure(figsize=(12, 6))
            plt.barh(df['板块名称'], df['涨跌幅'], color='blue')
            plt.title("概念板块涨跌幅", fontproperties=font_prop)
            plt.xlabel("涨跌幅", fontproperties=font_prop)
            plt.ylabel("板块名称", fontproperties=font_prop)
            plt.grid(True)
            plt.savefig("概念板块涨跌幅图.png")
            plt.close()
            print("[INFO] 概念板块涨跌幅图已生成：概念板块涨跌幅图.png")


def main():
    # 测试股票代码
    stock_code = "300624"
    print("[INFO] 测试开始...")
    stock_data = fetch_stock_data(stock_code)

    if stock_data:
        # 保存数据到单独的文件
        save_data_by_api(stock_data)

        # 为每组数据生成图表
       # generate_charts(stock_data)
    else:
        print("[ERROR] 数据获取失败，请检查接口或代码。")


if __name__ == "__main__":
    main()