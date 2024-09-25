import pandas as pd
from pathlib import Path

# 读取Excel文件
file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\文件管理_SJ.xlsx'
sheet_name = '文件管理'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 获取需要的列
filenames_column = df['文件名（编码）']

# 指定输出目录
output_dir = Path(r'C:\Users\JA085914\Desktop\PY\文件管理\输出文件夹')

# 如果输出目录不存在则创建
output_dir.mkdir(parents=True, exist_ok=True)

# 遍历文件名，创建新的Excel文件
for filename in filenames_column[0:]:  # 跳过第一行（标题行）
    new_file_path = output_dir / f"{filename}.xlsx"
    # 创建一个新的DataFrame，这里假设每个新文件只包含一个空的DataFrame
    new_df = pd.DataFrame()  # 或者你可以填充一些默认数据
    new_df.to_excel(new_file_path, index=False)