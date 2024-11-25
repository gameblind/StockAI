import re
from PIL import Image
import pytesseract
import os
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        

def extract_text_from_image(image_path, lang="eng+chi_sim"):
    """
    使用 Tesseract OCR 从图像中提取文本
    Args:
        image_path (str): 图像文件路径
        lang (str): OCR 语言
    Returns:
        str: 提取的文本内容
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)  # 支持多语言
        print("=== 提取的文本内容 ===")
        print("OCR提取的文本: ...")
        print("=====================")
        return text
    except Exception as e:
        print(f"提取文本失败: {e}")
        return None
    
import re

def extract_stock_info(text):
    """
    从 OCR 提取的文本中解析股票信息
    Args:
        text (str): OCR 提取的文本
    Returns:
        dict: 包含股票名称和代码的字典
    """
    stock_info = {"code": None, "name": None}
    try:
        # 匹配股票代码（6位数字，可能带有 .SZ 或 .SH 后缀）
        code_match = re.search(r'\b\d{6}(?:\.SZ|\.SH)?\b', text)
        if code_match:
            stock_info["code"] = code_match.group()

            # 匹配代码附近的中括号内容
            context_start = max(0, code_match.start() - 50)  # 向前 50 字符
            context_end = min(len(text), code_match.end() + 50)  # 向后 50 字符
            context = text[context_start:context_end]

            # 查找中括号中的内容，支持空格，并去除多余空格
            bracket_match = re.search(r'\[([\u4e00-\u9fa5\s]+)\]', context)
            if bracket_match:
                raw_name = bracket_match.group(1).strip()
                stock_info["name"] = re.sub(r'\s+', '', raw_name)  # 去除中括号内容中的多余空格

        # 打印调试信息
        print("=== OCR解析的股票信息 ===")
        print(f"股票代码: {stock_info['code']}")
        print(f"股票名称: {stock_info['name']}")
        print("=====================")

        return stock_info
    except Exception as e:
        print(f"解析股票信息失败: {e}")
        return None
        

# 测试代码
if __name__ == "__main__":
    # 示例图像路径
    image_path = "example_stock_image.png"

    # 提取文本
    ocr_text = extract_text_from_image(image_path)

    if ocr_text:
        # 解析股票信息
        stock_info = extract_stock_info(ocr_text)
        print("解析的股票信息：")
        print(stock_info)