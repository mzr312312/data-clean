import os
import pandas as pd
from datetime import datetime

# 设置标题行数（可以是1、2或3）
TITLE_ROWS = 2  # <<< 修改这个值来设置标题行数

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 输入文件夹路径（相对路径）
input_folder = os.path.join(script_dir, '../../PY/数据处理/26.合并本文件夹内的所有数据表')

# 输出文件路径（合并后的Excel）
output_folder = os.path.join(script_dir, '../../PY/数据处理')
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(output_folder, f'合并文件_{timestamp}.xlsx')

# 收集所有Excel文件
excel_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

# 存放DataFrame的列表
all_data = []

# 读取每个Excel文件
for file in excel_files:
    file_path = os.path.join(input_folder, file)

    # 读取Excel文件
    df = pd.read_excel(file_path, header=None)  # 不自动识别header

    # 提取标题行（前TITLE_ROWS行）
    title = df.iloc[:TITLE_ROWS]

    # 合并标题行为一行（适用于多行标题）
    combined_title = title.apply(lambda row: ' '.join(row.astype(str)), axis=0)

    # 设置列名
    df.columns = combined_title.tolist()

    # 去除原始标题行的内容
    data_part = df.iloc[TITLE_ROWS:]

    # 添加到总数据中
    all_data.append(data_part)

# 合并所有数据
final_df = pd.concat(all_data, ignore_index=True)

# 写入Excel文件
final_df.to_excel(output_file, index=False)

print(f"✅ 合并完成！输出文件为：{output_file}")