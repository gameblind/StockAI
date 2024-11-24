import os

def print_directory_structure(directory, indent=0):
    """
    打印目录及其子目录和文件的结构
    Args:
        directory (str): 根目录路径
        indent (int): 缩进级别
    """
    for item in os.listdir(directory):
        # 获取当前项的完整路径
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print("  " * indent + f"📁 {item}/")
            # 递归打印子目录
            print_directory_structure(item_path, indent + 1)
        else:
            print("  " * indent + f"📄 {item}")

if __name__ == "__main__":
    # 获取当前脚本所在目录作为项目根目录
    project_root = os.path.abspath(os.path.dirname(__file__))
    print(f"项目目录结构 ({project_root}):")
    print_directory_structure(project_root)