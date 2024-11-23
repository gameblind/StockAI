import os
from src.ocr.ocr_processor import extract_text_from_image, extract_stock_info

def test_ocr():
    # 示例截图路径
    image_path = "screenshots/sample_screenshot.png"

    # 检查截图是否存在
    if not os.path.exists(image_path):
        print(f"测试图片未找到: {image_path}")
        return

    # 1. 提取文本内容
    text = extract_text_from_image(image_path)
    if text:
        print("提取的文本内容：")
        print(text)
    else:
        print("未能提取到文本内容。")

    # 2. 提取股票信息
    stock_info = extract_stock_info(text)
    if stock_info:
        print("解析的股票信息：")
        print(stock_info)
    else:
        print("未能解析出有效的股票信息。")

if __name__ == "__main__":
    test_ocr()
    