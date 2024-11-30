import os

def save_directory_structure(directory, output_file, indent=0):
    """
    保存目录及其子目录和文件的结构到文件
    Args:
        directory (str): 根目录路径
        output_file (str): 输出文件路径
        indent (int): 缩进级别
    """
    with open(output_file, "a") as file:
        for item in os.listdir(directory):
            # 获取当前项的完整路径
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                file.write("  " * indent + f"📁 {item}/\n")
                # 递归保存子目录
                save_directory_structure(item_path, output_file, indent + 1)
            else:
                file.write("  " * indent + f"📄 {item}\n")

if __name__ == "__main__":
    # 获取当前脚本所在目录作为项目根目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    output_file = os.path.join(project_root, "project_structure.txt")

    # 清空之前的内容
    with open(output_file, "w") as file:
        file.write(f"项目目录结构 ({project_root}):\n")

    # 保存目录结构
    save_directory_structure(project_root, output_file)
    print(f"目录结构已保存到 {output_file}")