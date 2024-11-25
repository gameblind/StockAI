from PIL import ImageGrab
from datetime import datetime
import os
import sys

# 添加项目根目录到 sys.path
if __name__ == "__main__" and "src" not in sys.path:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# 创建子文件夹
def create_screenshot_folder(folder_name="screenshots"):
    """
    创建用于存放截图的子文件夹
    Args:
        folder_name (str): 子文件夹名称
    Returns:
        str: 子文件夹路径
    """
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def capture_fullscreen(folder_name=None):
    """
    使用 Pillow 截屏并保存到文件
    Args:
        folder_name (str): 截图保存文件夹
    Returns:
        str: 保存的文件路径
    """
    try:
        # 如果没有提供路径，则保存到子文件夹中
        folder_path = create_screenshot_folder(folder_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")

        # 截取全屏并保存
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        print(f"全屏截图成功，保存路径: {save_path}")
        return save_path
    except Exception as e:
        print(f"全屏截图失败: {e}")
        return None