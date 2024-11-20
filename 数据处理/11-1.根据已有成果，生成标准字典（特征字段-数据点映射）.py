"""
说明：
该脚本用于根据已有成果生成标准字典（特征字段-数据点映射）。它会从指定的Excel文件中加载现有的标准字典，并通过遍历指定文件夹中的所有Excel文件更新该字典。最终，它将更新后的标准字典保存回原始文件中。

功能：
1. 加载现有标准字典。
2. 遍历给定文件夹中的Excel文件，并更新标准字典。
3. 去重和清理标准字典中的空值。
4. 保存更新后的标准字典到指定的Excel文件。

原料池：
“原料池”是存放原材料信息的Excel文件集合。这些文件包含了需要更新的特征字段，通常包括不同的特征名称及其对应的标准名称。在使用脚本时，确保原料池中的文件格式与预期一致，文件应包含'标准名称'和'特征字段'等必要列。脚本将根据这些信息更新标准字典。

使用方法：
1. 确保已安装所需的Python库，包括pandas和numpy。
2. 修改脚本中的路径，以符合实际文件结构：
   - `existing_standard_dict_file`：现有标准字典的Excel文件路径。
   - `raw_material_folder`：存放需要处理的原料池Excel文件的文件夹路径。
3. 根据需要修改工作表名称或索引：
   - `worksheet_name_or_index`：可以指定工作表的名称或索引。
   - 当前来说，worksheet_name_or_index = 0的意思是：“选择第一个工作表”，无论这个工作表叫什么名字，都将被处理。
   - 文件名无所谓，只要在"原料池"文件夹中有相应的Excel文件即可。
4. 执行脚本，标准字典将被更新并保存。

注意事项：
- 确保Excel文件格式正确，包含'标准名称'和'特征字段'等必要列。
- 如果标准字典的Excel文件丢失，将返回一个空字典。
- 更新记录时间戳将被添加到标准字典中。
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np

# 设置待更新的标准字典的文件路径
existing_standard_dict_file = r'../../PY/数据处理/12.利用标准字典进行字段匹配(莱文斯坦距离)/标准字典（特征字段-数据点映射）.xlsx'
# 设置原料池文件夹路径
raw_material_folder = r'../../PY/数据处理/12.利用标准字典进行字段匹配(莱文斯坦距离)/原料池'

# 指定工作表名称或索引
worksheet_name_or_index = 0  # index=0,表示是sheet页的index=0，即第一个sheet页


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
