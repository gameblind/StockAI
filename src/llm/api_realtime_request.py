import asyncio
import websockets
import json
import os
import base64
from pydub import AudioSegment
import io
import logging
from datetime import datetime

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 全局变量，用于存储增量音频
audio_chunks = []


def load_config():
    """
    加载 settings.json 配置文件。
    Returns:
        dict: 配置文件内容。
    """
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/settings.json"))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)


def convert_https_to_wss(url):
    """
    将 HTTPS URL 转换为 WSS URL。
    """
    if url.startswith("https://"):
        return url.replace("https://", "wss://")
    elif url.startswith("http://"):
        return url.replace("http://", "ws://")
    else:
        raise ValueError(f"Invalid URL format: {url}")


def save_audio_file(audio_data_list, output_file):
    """
    保存增量音频数据为完整的 WAV 文件。
    Args:
        audio_data_list (list): 增量音频数据的 Base64 编码列表。
        output_file (str): 保存文件的路径。
    """
    try:
        # 解码并拼接所有增量音频
        audio_data = b"".join(base64.b64decode(chunk) for chunk in audio_data_list)

        # 将拼接后的 PCM 数据保存为 WAV 格式
        audio = AudioSegment(
            data=audio_data,
            sample_width=2,  # 16-bit PCM
            frame_rate=24000,
            channels=1
        )
        audio.export(output_file, format="wav")
        logging.info(f"Audio response saved to: {output_file}")
    except Exception as e:
        logging.error(f"Failed to save audio response: {e}")


async def receive_responses(ws):
    """
    接收并处理响应，并将音频增量数据保存为文件。
    """
    global audio_chunks

    async for message in ws:
        response = json.loads(message)

        # 日志记录简化
        logging.info(f"Response received with type: {response.get('type')}")

        # 处理增量音频响应
        if response.get("type") == "response.audio.delta":
            delta_audio = response.get("delta", "")
            if delta_audio:
                audio_chunks.append(delta_audio)
                logging.info("Audio chunk received and appended.")

        # 处理会话结束信号
        elif response.get("type") == "response.done":
            logging.info("Final response received. Saving audio file...")

            # 保存完整音频
            output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_folder, f"output_response_{timestamp}.wav")
            save_audio_file(audio_chunks, output_path)

            # 清空音频块
            audio_chunks = []


async def start_realtime_session(audio_file_path=None, text_message=None, model="gpt-4o-realtime-preview-2024-10-01"):
    """
    开启实时会话，支持发送音频或文本消息。
    """
    # 加载配置
    config = load_config()
    api_key = config["api_config"]["api_key"]
    base_url = config["api_config"]["api_url"]

    ws_url = convert_https_to_wss(base_url) + f"/v1/realtime?model={model}"
    headers = [
        ("Authorization", f"Bearer {api_key}"),
        ("OpenAI-Beta", "realtime=v1")
    ]

    try:
        logging.info(f"Connecting to WebSocket: {ws_url}")
        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            logging.info("Connected to WebSocket.")

            # 发送音频或文本消息
            if audio_file_path:
                await send_audio_message(ws, audio_file_path)
            elif text_message:
                await send_text_message(ws, text_message)

            # 接收响应
            await receive_responses(ws)

    except Exception as e:
        logging.error(f"An error occurred: {e}")


async def send_audio_message(ws, audio_file_path):
    """
    发送音频对话事件。
    """
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()

    pcm_audio = convert_audio_to_pcm(audio_bytes)
    base64_audio = base64.b64encode(pcm_audio).decode()

    audio_event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "audio": base64_audio
                }
            ]
        }
    }

    await ws.send(json.dumps(audio_event))
    logging.info("Audio message sent.")
    await ws.send(json.dumps({"type": "response.create"}))
    logging.info("Response request sent.")


async def send_text_message(ws, text):
    """
    发送文本对话事件。
    """
    text_event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": text
                }
            ]
        }
    }

    await ws.send(json.dumps(text_event))
    logging.info(f"Text message sent: {text}")
    await ws.send(json.dumps({"type": "response.create"}))
    logging.info("Response request sent.")


def convert_audio_to_pcm(audio_bytes):
    """
    将音频数据转换为 24kHz PCM 16-bit。
    """
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2)
    return audio.raw_data


if __name__ == "__main__":
    AUDIO_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/input.wav"))
    TEXT_MESSAGE = "请大笑着回答"  # 填入文本内容或保持为 None

    try:
        asyncio.run(start_realtime_session(audio_file_path=AUDIO_FILE_PATH, text_message=TEXT_MESSAGE))
    except Exception as e:
        logging.error(f"An error occurred: {e}")