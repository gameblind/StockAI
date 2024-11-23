import os
import base64
import requests
from config.settings import CONFIG_MANAGER  # 修正导入路径

def upload_image_to_github(image_path, upload_path):
    """
    上传图片到 GitHub 仓库，并返回图片的 Raw URL。
    """
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