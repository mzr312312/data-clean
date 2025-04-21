import os
import pandas as pd
from datetime import datetime

# 设置路径
standard_dict_file = r'../../PY/数据处理/11.根据已有成果，生成标准字典（特征字段-数据点映射）/标准字典（特征字段-数据点映射）.xlsx'
output_folder = os.path.dirname(standard_dict_file)


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


def check_duplicate_aliases(standard_dict):
    """检查标准字典中的错误项（别名同时属于两个或两个以上标准字段）"""
    alias_to_standards = {}

    # 构建别名到标准字段的映射
    for standard_name, aliases in standard_dict.items():
        for alias in aliases:
            if alias not in alias_to_standards:
                alias_to_standards[alias] = set()
            alias_to_standards[alias].add(standard_name)

    # 检查哪些别名属于两个或两个以上的标准字段
    duplicate_aliases = {alias: standards for alias, standards in alias_to_standards.items() if len(standards) > 1}

    return duplicate_aliases


def save_check_results(duplicate_aliases, output_folder):
    """保存检查结果到新的Excel文件，并附加时间戳"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_folder, f'检查结果_{timestamp}.xlsx')

    data = []
    for alias, standards in duplicate_aliases.items():
        data.append([alias, ', '.join(standards)])

    df = pd.DataFrame(data, columns=['特征字段', '关联的标准字段'])
    df.to_excel(output_file, index=False)

    return output_file


# 主程序
if __name__ == "__main__":
    # 加载现有的标准字典
    standard_dict = load_standard_dictionary(standard_dict_file)

    # 检查标准字典中的错误项
    duplicate_aliases = check_duplicate_aliases(standard_dict)

    # 保存检查结果到新的Excel文件，并附加时间戳
    output_file = save_check_results(duplicate_aliases, output_folder)

    print(f"检查结果已保存到 {output_file}")
