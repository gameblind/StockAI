import pandas as pd
import json

def excel_to_json(excel_file, json_file):
    """
    将 Excel 文件中的每一行转换为 JSON 文件。
    
    :param excel_file: str, 输入的 Excel 文件路径。
    :param json_file: str, 输出的 JSON 文件路径。
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_file)
        
        # 检查是否有数据
        if df.empty:
            raise ValueError("Excel 文件为空")
        
        # 将 DataFrame 转换为字典列表
        data_list = df.to_dict(orient='records')
        
        # 将字典列表写入 JSON 文件
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)
        
        print(f"转换成功！JSON 文件已保存到: {json_file}")
    
    except Exception as e:
        print(f"发生错误: {e}")

# 使用示例
# 输入 Excel 文件路径
excel_file_path = "project_tools/dictionary.xlsx"
# 输出 JSON 文件路径
json_file_path = "project_tools/apis.json"

# 调用函数
excel_to_json(excel_file_path, json_file_path)