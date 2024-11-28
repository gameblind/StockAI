import os
import sys
import json
import http.client
from base64 import b64decode

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


# 加载配置
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


# 语音生成函数
def generate_speech(text, model="tts-1-hd", voice="onyx", response_format="mp3", speed=1.0, output_file="output_audio.mp3"):
    """
    调用 TTS API 生成语音并保存为音频文件。

    Args:
        text (str): 要生成语音的文本。要生成音频的文本。最大长度为4096个字符。
        model (str): 使用的 TTS 模型，默认为 "tts-1"可用的 TTS 模型之一:tts-1 或 tts-1-hd。
        voice (str): 语音风格，默认为 "alloy、echo、fable、onyx、nova 和 shimmer。"。
        response_format (str): 返回音频的格式（mp3, opus, aac, flac）。
        speed (float): 音频播放速度，范围 0.25 到 4.0。
        output_file (str): 输出音频文件路径。
    """
    # 加载 API 配置
    config = load_config()
    api_key = config["api_config"]["api_key"]
    api_url = config["api_config"]["api_url"]

    # 解析 API 主机名和路径
    if not api_url.startswith("https://"):
        raise ValueError("API URL 必须以 https:// 开头")
    host = api_url.replace("https://", "").split("/")[0]
    endpoint = "/v1/audio/speech"

    # 请求体
    payload = json.dumps({
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
        "speed": speed
    })

    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 发送请求
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", endpoint, payload, headers)
        res = conn.getresponse()

        if res.status != 200:
            raise Exception(f"API 请求失败，状态码: {res.status}, 原因: {res.reason}")

        # 读取返回的音频数据
        audio_data = res.read()
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output", output_file))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio_data)
        print(f"语音已保存到 {output_path}")
    except Exception as e:
        print(f"请求失败: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    # 测试文本
    #TEST_TEXT = "In a world where shadows linger and dreams collide, there lies a story untold. A tale of love, loss, and redemption. They say time heals all wounds, but some scars run deeper than the ocean, etched into the soul like whispers of forgotten storms. I’ve walked through the fire, seen the light fade into darkness, yet here I stand, unbroken, a testament to the resilience of the human spirit. This is not just my story—it’s ours. A story of hope, a story of us."
    TEST_TEXT = "在这个光影交错、梦境交汇的世界里，隐藏着一个未曾诉说的故事。一个关于爱、关于失落、关于救赎的故事。有人说，时间可以治愈一切，但有些伤痕比海洋还深，刻在灵魂深处，如同被遗忘的风暴低语。我曾穿越烈火，见证光明消失在黑暗之中，但如今我依然站在这里，不曾倒下，这便是人类精神的韧性。这不仅是我的故事，它是我们的故事。一个关于希望的故事，一个关于我们的故事。"
    try:
        # 调用函数生成语音，格式为 mp3
        generate_speech(TEST_TEXT, response_format="mp3", output_file="output_audio.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")