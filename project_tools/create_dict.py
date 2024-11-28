import pandas as pd
import json

def excel_to_nested_json(excel_file, json_file, main_sheet, sub_sheet, key_column):
    # 读取主表和子表
    main_df = pd.read_excel(excel_file, sheet_name=main_sheet, engine='openpyxl')
    sub_df = pd.read_excel(excel_file, sheet_name=sub_sheet, engine='openpyxl')
    
    # 创建主表的字典结构
    main_records = main_df.to_dict(orient='records')
    
    # 按外键分组子表数据
    sub_grouped = sub_df.groupby(key_column).apply(lambda x: x.to_dict(orient='records')).to_dict()
    
    # 将子表嵌套到主表中
    for record in main_records:
        record['fields'] = sub_grouped.get(record[key_column], [])
    
    # 保存为 JSON 文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(main_records, f, ensure_ascii=False, indent=4)
    
    print(f"嵌套 JSON 数据已成功保存到 {json_file}")

# 文件路径和参数
excel_file = "dictionary.xlsx"  # 替换为你的 Excel 文件名
json_file = "output_nested.json"  # 转换后的 JSON 文件名
main_sheet = "apis"  # 主表 Sheet 名
sub_sheet = "fields"  # 子表 Sheet 名
key_column = "API Key Combined"  # 主键和外键字段名

# 调用函数
excel_to_nested_json(excel_file, json_file, main_sheet, sub_sheet, key_column)