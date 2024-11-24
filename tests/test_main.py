import os
from src.upload_images.upload_images import upload_image_to_github

def test_upload_image():
    image_path = "screenshots/sample_screenshot.png"
    upload_path = "screenshots/sample_screenshot.png"  # 仓库中的目标路径
    try:
        raw_url = upload_image_to_github(image_path, upload_path)
        print(f"图片上传成功！URL: {raw_url}")
    except Exception as e:
        print(f"图片上传失败: {e}")

if __name__ == "__main__":
    test_upload_image()