import pandas as pd
import time
import os

# 定义文件路径
file_path = r'..\PY\数据处理\18.把一个sheet页里所有列合并成1列.xlsx'
output_dir = os.path.dirname(file_path)
output_file_name = f'合并成1列_{int(time.time())}.xlsx'  # 带时间戳的文件名
output_path = os.path.join(output_dir, output_file_name)

# 读取Excel文件
df = pd.read_excel(file_path)

# 合并所有列成一列，去掉第一行的列名
merged_column = pd.Series(df.values.ravel()).dropna()  # 使用ravel()将二维数组变为一维数组，并去掉空值

# 创建新的DataFrame
result_df = pd.DataFrame(merged_column, columns=['合并后'])

# 保存为新的Excel文件
result_df.to_excel(output_path, index=False)

print(f'文件已保存到: {output_path}')
