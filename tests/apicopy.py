import os
import sys

# 动态添加 src 路径，便于导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from upload_images.upload_images import upload_image_to_github
from llm.api_request import submit_request_to_api

if __name__ == "__main__":
    # 本地图片路径和 GitHub 上传路径
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../screenshots/sample_screenshot.png"))
    upload_path = "images/sample_screenshot.png"

    # AI API 的模型名称和提示词
    model_name = "gpt-4-all"
    prompt_text = "帮我分析图中股票走势："

    try:
        # Step 1: 上传图片到 GitHub
        print("Uploading image to GitHub...")
        image_url = upload_image_to_github(image_path, upload_path)
        print(f"Image uploaded successfully to GitHub: {image_url}")
    except Exception as e:
        print(f"Error during image upload: {e}")
        sys.exit(1)  # 中止程序

    try:
        # Step 2: 调用 AI API 分析图片
        print("Submitting request to AI API...")
        result = submit_request_to_api(model_name, prompt_text, image_url)
        print("AI API Response:", result)
    except Exception as e:
        print(f"Error during API request: {e}")
        sys.exit(1)  # 中止程序