import os
import base64
import requests
from settings import CONFIG_MANAGER

def upload_image_to_github(image_path, upload_path):
    """
    上传图片到 GitHub 仓库，并返回图片的 Raw URL。

    Args:
        image_path (str): 本地图片路径。
        upload_path (str): 上传到仓库的路径（如 "images/sample.png"）。

    Returns:
        str: 图片的 Raw URL。
    """
    # 从配置文件加载 GitHub 配置信息
    github_token = CONFIG_MANAGER.get("github_token")
    repo_owner = "gameblind"  # GitHub 用户名
    repo_name = "image-storage"  # GitHub 仓库名
    github_api_url_template = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    github_api_url = github_api_url_template.format(owner=repo_owner, repo=repo_name, path=upload_path)

    # 检查文件是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    # 读取图片并进行 Base64 编码
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # 构造 GitHub API 请求
    headers = {"Authorization": f"Bearer {github_token}"}
    data = {
        "message": f"Upload {os.path.basename(image_path)} via API",
        "content": encoded_image
    }

    # 发送请求
    response = requests.put(github_api_url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # 检查上传结果并生成 Raw URL
    if "content" not in result:
        raise Exception(f"Image upload failed: {result.get('message')}")
    raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{upload_path}"
    return raw_url

# 测试代码（如果需要单独运行此模块）
if __name__ == "__main__":
    # 示例：本地图片路径和上传路径
    image_path = os.path.join("screenshots", "sample_screenshot.png")
    upload_path = "images/sample_screenshot.png"

    try:
        raw_url = upload_image_to_github(image_path, upload_path)
        print(f"Image uploaded successfully to GitHub: {raw_url}")
    except Exception as e:
        print(f"An error occurred: {e}")