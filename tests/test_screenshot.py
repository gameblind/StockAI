from src.screenshot.screen_capture import capture_fullscreen, capture_window
import os

def test_capture_fullscreen():
    """
    测试全屏截图功能
    """
    screenshot_path = capture_fullscreen("test_fullscreen.png")
    assert os.path.exists(screenshot_path), "全屏截图失败！"
    print("全屏截图测试通过！")

def test_capture_window():
    """
    测试窗口截图功能
    """
    region = {"top": 100, "left": 100, "width": 800, "height": 600}
    screenshot_path = capture_window(region, "test_window_screenshot.png")
    assert os.path.exists(screenshot_path), "窗口截图失败！"
    print("窗口截图测试通过！")

if __name__ == "__main__":
    test_capture_fullscreen()
    test_capture_window()