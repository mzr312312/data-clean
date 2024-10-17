import os
import pandas as pd
from datetime import datetime
import numpy as np

# 设置路径
existing_standard_dict_file = r'C:\Users\JA085914\Desktop\PY\数据处理\11.根据已有成果，生成标准字典（特征字段-数据点映射）\标准字典（特征字段-数据点映射）.xlsx'
raw_material_folder = r'C:\Users\JA085914\Desktop\PY\数据处理\11.根据已有成果，生成标准字典（特征字段-数据点映射）\原料池'

# 指定工作表名称或索引
worksheet_name_or_index = '原料池'  # 或者使用索引：worksheet_name_or_index = 1


def load_standard_dictionary(file_path):
    """加载现有的标准字典"""
    try:
        df = pd.read_excel(file_path)
        standard_dict = {}
        for _, row in df.iterrows():
            standard_name = row['标准名称']
            aliases = [alias for alias in row[1:] if pd.notna(alias)]
            if standard_name not in standard_dict:
                standard_dict[standard_name] = aliases
            else:
                standard_dict[standard_name].extend(aliases)
        return standard_dict
    except FileNotFoundError:
        return {}


def update_standard_dictionary(standard_dict, import_file_path, worksheet_name_or_index):
    """更新标准字典并记录时间戳"""
    import_df = pd.read_excel(import_file_path, sheet_name=worksheet_name_or_index)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for _, row in import_df.iterrows():
        standard_name = row['标准名称']
        alias = row['特征字段']
        if standard_name not in standard_dict:
            standard_dict[standard_name] = [alias]
        elif alias not in standard_dict[standard_name]:
            standard_dict[standard_name].append(alias)

    if '更新时间' not in standard_dict:
        standard_dict['更新时间'] = []
    standard_dict['更新时间'].append(timestamp)

    return standard_dict


def remove_duplicates_and_empty(standard_dict):
    for key, aliases in standard_dict.items():
        # 处理 nan 值
        if not isinstance(aliases, list):
            raise ValueError(f"Invalid value type for key '{key}': {aliases}")

        # 将 nan 转换为字符串 "nan"
        aliases = [str(alias) if isinstance(alias, float) and np.isnan(alias) else alias for alias in aliases]

        # 确保列表中的每个元素都是字符串
        if not all(isinstance(alias, str) for alias in aliases):
            raise ValueError(f"Invalid value type for key '{key}': {aliases}")

        unique_aliases = list(set(aliases))  # 去重
        standard_dict[key] = [alias.strip() for alias in unique_aliases if alias.strip()]  # 移除空字符串

# 示例调用
standard_dict = {
    'nan': [np.nan, 'abc', 'def'],
    'key1': ['abc', 'def', 'ghi']
}

remove_duplicates_and_empty(standard_dict)
print(standard_dict)

def save_standard_dictionary(standard_dict, file_path):
    """保存标准字典到Excel文件"""
    max_aliases = max(len(aliases) for aliases in standard_dict.values())
    columns = ['标准名称'] + [f'别名{i + 1}' for i in range(max_aliases)]

    data = []
    for standard_name, aliases in standard_dict.items():
        if standard_name != '更新时间':
            row = [standard_name] + aliases + [None] * (max_aliases - len(aliases))
            data.append(row)

    for timestamp in standard_dict.get('更新时间', []):
        data.append(['更新时间', timestamp] + [None] * (max_aliases - 1))

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(file_path, index=False)


# 主程序
if __name__ == "__main__":
    # 加载现有的标准字典
    standard_dict = load_standard_dictionary(existing_standard_dict_file)

    # 遍历“原料池”文件夹中的所有Excel文件
    for filename in os.listdir(raw_material_folder):
        if filename.endswith('.xlsx'):
            import_file_path = os.path.join(raw_material_folder, filename)
            standard_dict = update_standard_dictionary(standard_dict, import_file_path, worksheet_name_or_index)

    # 去除重复项并删除空格
    remove_duplicates_and_empty(standard_dict)

    # 保存更新后的标准字典到现有的文件
    save_standard_dictionary(standard_dict, existing_standard_dict_file)

    print(f"标准字典已更新并保存到 {existing_standard_dict_file}")
