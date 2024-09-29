# 代码功能说明：
# 1.需要加载一个【过程文件】标准字典的导入文件.xlsx文件，该文件包含了需要导入的标准名称和特征字段，这个文件其实是我梳理完成的所有数据点清单文件复制出来的；
# 2.需要加载一个标准字典（特征字段-数据点映射）.xlsx文件，这个文件每行代表一个标准名称，每一列代表一个特征字段，值代表该标准名称对应的特征字段，多次运行本代码，可以继续添加新的数据点，并且会记录时间戳；
# 3.需要设置的部分为：existing_standard_dict_file（标准字典文件路径）、import_files（导入文件路径列表），其余不需要修改；

import pandas as pd
from datetime import datetime

# 设置路径
existing_standard_dict_file = r'C:\Users\JA085914\Desktop\PY\数据处理\11.根据已有成果，生成标准字典（特征字段-数据点映射）\标准字典（特征字段-数据点映射）.xlsx'
import_files = [r'C:\Users\JA085914\Desktop\PY\数据处理\11.根据已有成果，生成标准字典（特征字段-数据点映射）\【过程文件】标准字典的导入文件.xlsx']


# ⬆️添加更多文件,例如，后跟, 'import_file2.xlsx', 'import_file3.xlsx'

def load_standard_dictionary(file_path):
    """加载现有的标准字典"""
    try:
        df = pd.read_excel(file_path)
        standard_dict = {}
        for _, row in df.iterrows():
            standard_name = row['标准名称']
            aliases = [alias for alias in row[1:] if pd.notna(alias)]  # 获取所有非空的别名
            if standard_name not in standard_dict:
                standard_dict[standard_name] = aliases
            else:
                standard_dict[standard_name].extend(aliases)
        return standard_dict
    except FileNotFoundError:
        return {}


def update_standard_dictionary(standard_dict, import_file_path):
    """更新标准字典并记录时间戳"""
    import_df = pd.read_excel(import_file_path)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for _, row in import_df.iterrows():
        standard_name = row['标准名称']
        alias = row['特征字段']
        if standard_name not in standard_dict:
            standard_dict[standard_name] = [alias]
        elif alias not in standard_dict[standard_name]:
            standard_dict[standard_name].append(alias)

    # 记录时间戳
    if '更新时间' not in standard_dict:
        standard_dict['更新时间'] = []
    standard_dict['更新时间'].append(timestamp)

    return standard_dict


def save_standard_dictionary(standard_dict, file_path):
    """保存标准字典到Excel文件"""
    max_aliases = max(len(aliases) for aliases in standard_dict.values() if isinstance(aliases, list))
    columns = ['标准名称'] + [f'别名{i + 1}' for i in range(max_aliases)]

    data = []
    for standard_name, aliases in standard_dict.items():
        if standard_name != '更新时间':
            # 保留已有的别名，并在后续列中补充新的别名
            existing_row = None
            if 'data' in locals() and len(data) > 0:
                for row in data:
                    if row[0] == standard_name:
                        existing_row = row
                        break

            if existing_row:
                # 如果已经有该标准名称的行，则合并别名
                existing_aliases = existing_row[1:]
                new_aliases = [alias for alias in aliases if alias not in existing_aliases]
                row = [standard_name] + (existing_aliases + new_aliases + [None] * max_aliases)[:max_aliases]
            else:
                # 如果没有该标准名称的行，则创建新行
                row = [standard_name] + (aliases + [None] * max_aliases)[:max_aliases]

            data.append(row)

    # 将时间戳单独保存
    for timestamp in standard_dict.get('更新时间', []):
        data.append(['更新时间', timestamp] + [None] * (max_aliases - 1))

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(file_path, index=False)


# 主程序
if __name__ == "__main__":
    # 加载现有的标准字典
    standard_dict = load_standard_dictionary(existing_standard_dict_file)

    # 逐个处理导入文件
    for import_file in import_files:
        standard_dict = update_standard_dictionary(standard_dict, import_file)

    # 保存更新后的标准字典到现有的文件
    save_standard_dictionary(standard_dict, existing_standard_dict_file)

    print(f"标准字典已更新并保存到 {existing_standard_dict_file}")