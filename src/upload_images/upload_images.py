import os
import base64
import requests
import json
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def load_config():
    """加载配置文件"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/settings.json"))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)

CONFIG = load_config()

def check_existing_file(github_api_url, headers):
    """
    检查文件是否已存在，并返回 SHA 值。
    Args:
        github_api_url (str): 文件的 API URL。
        headers (dict): 请求头信息。
    Returns:
        str: 文件的 SHA 值。如果文件不存在，则返回 None。
    """
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        return response.json().get("sha")
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"检查文件是否存在时出错: {response.status_code} - {response.text}")

def upload_image_to_github(image_path, upload_path):
    """
    上传图片到 GitHub 仓库，并返回图片的 Raw URL。
    """
    github_token = CONFIG.get("github_config").get("github_token")
    repo_owner = CONFIG.get("github_config").get("repo_owner")
    repo_name = CONFIG.get("github_config").get("repo_name")
    github_api_url_template = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    github_api_url = github_api_url_template.format(owner=repo_owner, repo=repo_name, path=upload_path)

    # 检查文件是否已存在
    headers = {"Authorization": f"Bearer {github_token}"}
    sha = check_existing_file(github_api_url, headers)

    # 读取图片并进行 Base64 编码
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件未找到: {image_path}")
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # 构造 GitHub API 请求
    data = {
        "message": f"Upload {os.path.basename(image_path)} via API",
        "content": encoded_image
    }
    if sha:
        data["sha"] = sha  # 如果文件已存在，添加 sha 值

    # 发送请求到 GitHub API
    response = requests.put(github_api_url, headers=headers, json=data)
    if response.status_code not in [200, 201]:
        raise Exception(f"图片上传失败: {response.status_code} - {response.text}")

    # 返回 Raw URL
    return f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{upload_path}"