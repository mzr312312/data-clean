import pandas as pd
from datetime import datetime

# 读取Excel文件的指定Sheet页
file_path = (r'D:\Factory\BOM清单V1.1(20240825).xlsx')
df = pd.read_excel(file_path, sheet_name='BOM')

# 打印列名以确认
print(df.columns)

# 获取当前日期-时间戳
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# 生成新的文件路径
new_file_path = f'{file_path[:-5]}_{timestamp}.xlsx'

# 列的数字序号
output_columns = [2, 4, 6]  # 输出1, 输出2, 输出3
input_columns = [10, 12, 14, 16, 18, 20, 22, 23, 24]  # 输入1, 输入2, 输入3, 输入4, 输入5, 输入6,生产设备1，生产设备2，生产设备3
output_quantity_columns = [3, 5, 7]  # 输出1数量, 输出2数量, 输出3数量
input_quantity_columns = [11, 13, 15, 17, 19, 21]  # 输入1数量, 输入2数量, 输入3数量, 输入4数量, 输入5数量, 输入6数量

# 处理输出列
for col in output_columns:
    column_name = df.columns[col]
    df[column_name] = df[column_name].apply(lambda x: 'none' if pd.isna(x) else x)

# 处理输入列
for col in input_columns:
    column_name = df.columns[col]
    df[column_name] = df[column_name].apply(lambda x: 'none' if pd.isna(x) else x)

# 处理输出数量列
for col in output_quantity_columns:
    column_name = df.columns[col]
    df[column_name] = df[column_name].apply(lambda x: 0 if pd.isna(x) else x)

# 处理输入数量列
for col in input_quantity_columns:
    column_name = df.columns[col]
    df[column_name] = df[column_name].apply(lambda x: 0 if pd.isna(x) else x)

# 保存修改后的Excel文件
with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='BOM', index=False)
