# 说明：
# 1. 输入文件(input_file_path)：特征字段输入文件，包含特征字段"列，这里输入的是各种个等待确定标准名称的特征字段。
# 2. 标准字典文件（dictionary_file_path）：标准字典文件，包含标准名称和别名，这里输入的是各种标准名称，以及其可能的别名。这里需要使用【11.根据已有成果，生成标准字典（特征字段-数据点映射）.py】，将已经完成的标准明-别名映射关系导入到标准字典文件中，不断更新标准字典文件。
# 3. 标准字典文件更新的越完善，本代码的准确定就越高（亲测有效）；
# 4. 本代码的匹配结果，也可以作为【11.根据已有成果，生成标准字典（特征字段-数据点映射）.py】的输入，用于更新标准字典文件。
# 5. 运行本代码，会生成一个Excel文件（output_file_path_template），包含输入文件中所有特征字段的匹配结果。
# 6. 生成的文件中的内容，可以复制回数据点清单（如：To-Internal_设备类型清单&数据点清单_压缩空气_SJ.xlsx）中，用于更新数据点清单中的数据点编码；

import pandas as pd
from fuzzywuzzy import process
from datetime import datetime

# ========== 手动调整的变量 ==========
# 输入和输出文件路径
input_file_path = r'C:\Users\JA085914\Desktop\PY\数据处理\12.利用标准字典进行字段匹配(莱文斯坦距离)\特征字段输入.xlsx'
dictionary_file_path = r'C:\Users\JA085914\Desktop\PY\数据处理\11.根据已有成果，生成标准字典（特征字段-数据点映射）\标准字典（特征字段-数据点映射）.xlsx'
output_file_path_template = r'C:\Users\JA085914\Desktop\PY\数据处理\12.利用标准字典进行字段匹配(莱文斯坦距离)\最新output_匹配结果_{timestamp}.xlsx'

# 特征字段列名和字典中的列名
feature_column_name = '特征字段'  # 输入文件中的列名
standard_name_column = '标准名称'  # 字典中的"标准名称"列

# 模糊匹配返回的候选数量
top_n_matches = 3


# ===================================


def load_data(input_file, dictionary_file):
    """加载输入数据和标准字典"""
    # 加载特征字段输入文件
    input_df = pd.read_excel(input_file)


    # 加载标准字典文件，并将所有别名列合并为一列，用于后续匹配
    dictionary_df = pd.read_excel(dictionary_file)

    return input_df, dictionary_df


def create_alias_mapping(dictionary_df):
    """创建别名到标准名称的映射表"""
    alias_to_standard_map = []

    for _, row in dictionary_df.iterrows():
        standard_name = row[standard_name_column]
        aliases = row.dropna().tolist()  # 获取该行所有非空值，包括"别名"和"标准名称"

        for alias in aliases:
            alias_to_standard_map.append((alias, standard_name))

    return alias_to_standard_map


def match_features_to_standard(input_df, alias_to_standard_map):
    """对输入特征字段进行匹配，返回最接近的3个候选项"""
    results = []

    for feature in input_df[feature_column_name]:
        # 预处理：确保 feature 是字符串，如果不是则转换为空字符串
        if not isinstance(feature, str):
            feature = str(feature) if not pd.isna(feature) else ""
        # 提取所有别名列表用于模糊匹配 (alias 是元组 (别名, 标准名称))
        all_aliases = [alias for alias, _ in alias_to_standard_map]

        # 使用fuzzywuzzy进行模糊匹配，返回与当前feature最接近的top_n_matches个结果
        matches = process.extract(feature, all_aliases, limit=top_n_matches)

        # 找到对应的 "标准名称"
        matched_standards = [next(standard for alias, standard in alias_to_standard_map if alias == match[0]) for match
                             in matches]

        results.append({
            feature_column_name: feature,
            '候选1': matched_standards[0] if len(matched_standards) > 0 else None,
            '候选2': matched_standards[1] if len(matched_standards) > 1 else None,
            '候选3': matched_standards[2] if len(matched_standards) > 2 else None,
        })

    return pd.DataFrame(results)


def save_results(result_df):
    """保存结果到Excel文件"""
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file_path = output_file_path_template.format(timestamp=timestamp_str)

    result_df.to_excel(output_file_path, index=False)
    print(f'结果已保存到: {output_file_path}')


if __name__ == "__main__":
    # 加载数据
    input_df, dictionary_df = load_data(input_file_path, dictionary_file_path)

    # 创建别名到“标准名称”的映射表
    alias_to_standard_map = create_alias_mapping(dictionary_df)

    # 对输入特征字段进行匹配并生成结果DataFrame
    result_df = match_features_to_standard(input_df, alias_to_standard_map)

    # 保存结果到Excel文件
    save_results(result_df)

