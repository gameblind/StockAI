import http.client
import json
import os
import logging
import time
from urllib.parse import urlparse
from urllib.request import urlretrieve

# 配置日志
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# 文件路径
TASKS_FILE = "output/tasks.json"

# 加载配置
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../config/settings.json")
    with open(config_path, "r") as f:
        return json.load(f)

# 加载任务 JSON 文件
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {}
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

# 保存任务 JSON 文件
def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# 添加新任务到 JSON 文件
def add_task_to_file(task_id, prompt):
    tasks = load_tasks()
    if task_id not in tasks:
        tasks[task_id] = {"prompt": prompt, "status": "submitted"}
        save_tasks(tasks)
        logging.info(f"Added task {task_id} to {TASKS_FILE}.")

# 更新任务状态
def update_task_status(task_id, status):
    tasks = load_tasks()
    if task_id in tasks:
        tasks[task_id]["status"] = status
        save_tasks(tasks)
        logging.info(f"Updated task {task_id} status to {status}.")

# 发送 POST 请求
def send_post_request(endpoint, payload, headers):
    config = load_config()
    base_url = config["api_config"]["api_url"].rstrip("/")  # 确保无尾随 "/"

    conn = http.client.HTTPSConnection(base_url.replace("https://", ""))
    logging.info(f"[DEBUG] Sending POST request to: {endpoint}")
    conn.request("POST", endpoint, json.dumps(payload), headers)

    response = conn.getresponse()
    return decode_response(response)

# 发送 GET 请求
def send_get_request(endpoint):
    config = load_config()
    base_url = config["api_config"]["api_url"].rstrip("/")  # 确保无尾随 "/"
    api_key = config["api_config"]["api_key"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    conn = http.client.HTTPSConnection(base_url.replace("https://", ""))
    logging.info(f"[DEBUG] Sending GET request to: {endpoint}")
    conn.request("GET", endpoint, headers=headers)
    response = conn.getresponse()
    return decode_response(response)

# 解码响应
def decode_response(response):
    raw_data = response.read()
    if response.headers.get("Content-Encoding") == "gzip":
        import gzip
        raw_data = gzip.decompress(raw_data)
    try:
        return json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        logging.error(f"Error decoding response: {e}")
        logging.error(f"Raw response content: {raw_data[:500]}")  # 打印前500字符
        raise

# 创建视频任务
def create_video_task(prompt, external_task_id="custom_task_001"):
    payload = {
        "model_name": "kling-v1",
        "prompt": prompt,
        "cfg_scale": 0.5,
        "mode": "std",
        "aspect_ratio": "16:9",
        "duration": "5",
        "external_task_id": external_task_id,
    }

    headers = {
        "Authorization": f"Bearer {load_config()['api_config']['api_key']}",
        "Content-Type": "application/json",
    }

    return send_post_request("/kling/v1/videos/text2video", payload, headers)

# 查询单个任务状态
def fetch_single_task_status(task_id):
    endpoint = f"/kling/v1/videos/text2video/{task_id}"
    return send_get_request(endpoint)

# 下载视频
def download_video(video_url, output_dir="output/videos"):
    os.makedirs(output_dir, exist_ok=True)
    video_name = os.path.basename(urlparse(video_url).path)
    output_path = os.path.join(output_dir, video_name)

    try:
        logging.info(f"Downloading video from: {video_url}")
        urlretrieve(video_url, output_path)
        logging.info(f"Video saved to: {output_path}")
    except Exception as e:
        logging.error(f"Failed to download video: {e}")

# 生成视频并记录任务
def generate_and_save_video(prompt):
    try:
        logging.info("Creating video task...")
        response = create_video_task(prompt)
        logging.info(f"[DEBUG] Response from create_video_task: {response}")

        if not response or "code" not in response or response["code"] != 0:
            raise ValueError(f"API returned an error: {response}")

        task_id = response["data"]["task_id"]
        logging.info(f"Video task created successfully. Task ID: {task_id}")
        add_task_to_file(task_id, prompt)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# 遍历 JSON 文件中的任务，下载完成的视频
def process_and_download_tasks():
    tasks = load_tasks()

    for task_id, info in tasks.items():
        if info["status"] in ["succeed", "downloaded"]:
            continue  # 跳过已处理的任务

        logging.info(f"Checking status for Task ID: {task_id}...")
        status_response = fetch_single_task_status(task_id)

        if not status_response or "data" not in status_response:
            logging.error(f"Failed to fetch status for task {task_id}.")
            continue

        task_status = status_response["data"]["task_status"]
        if task_status == "succeed":
            videos = status_response["data"]["task_result"]["videos"]
            for video in videos:
                download_video(video["url"])
            update_task_status(task_id, "downloaded")
        elif task_status == "failed":
            update_task_status(task_id, "failed")
        else:
            logging.info(f"Task {task_id} is still processing. Skipping...")

# 主函数
if __name__ == "__main__":
    PROMPT = input("Enter a prompt for video generation (leave empty to fetch tasks): ").strip()
    if PROMPT:
        generate_and_save_video(PROMPT)
    else:
        # fetch_single_task_status("Cji6L2dHrfoAAAAAAB3C6g")
        process_and_download_tasks()


#         model
# string 
# 可选
# prompt
# string 
# 必需
# 正向文本提示，必须，不能超过500个字符

# <= 500 字符
# negative_prompt
# string 
# 可选
# 负向文本提示，可选，不能超过200个字符

# <= 200 字符
# cfg_scale
# number 
# 可选
# 生成视频的自由度，可选，值越大，相关性越强，取值范围：[0,1]

# >= 0
# <= 1
# mode
# enum<string> 
# 可选
# 生成视频的模式，可选，枚举值：std（高性能）或 pro（高表现）

# 枚举值:
# std（高性能）
# pro（高表现）
# camera_control
# object 
# 可选
# 控制摄像机运动的协议，可选，未指定则智能匹配

# type
# string 
# 可选
# config
# object 
# 可选
# 包含六个字段，用于指定摄像机的运动或变化

# aspect_ratio
# enum<string> 
# 可选
# 生成视频的画面纵横比，可选，枚举值：16:9, 9:16, 1:1

# 枚举值:
# 16:9
# 9:16
# 1:1
# duration
# enum<string> 
# 可选
# 生成视频时长，单位秒，可选，枚举值：5，10

# 枚举值:
# 5
# 10
# callback_url
# string 
# 可选
# 本次任务结果回调通知地址，可选