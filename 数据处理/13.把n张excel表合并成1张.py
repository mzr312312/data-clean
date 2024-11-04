import pandas as pd
import os

# 设置文件路径
folder_path = 'path/to/your/excel/files'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 创建一个空的DataFrame用于存储合并后的数据
combined_df = pd.DataFrame()

# 遍历文件名列表
for file_name in file_names:
    # 构造完整文件路径
    file_path = os.path.join(folder_path, file_name)

    # 读取Excel文件，假设每个文件只有一个工作表
    temp_df = pd.read_excel(file_path)

    # 将当前文件的数据追加到combined_df
    combined_df = combined_df.append(temp_df, ignore_index=True)

# 将合并后的数据保存到新的Excel文件
output_file = 'combined_output.xlsx'
combined_df.to_excel(output_file, index=False)

print(f"合并完成！已保存至 {output_file}")