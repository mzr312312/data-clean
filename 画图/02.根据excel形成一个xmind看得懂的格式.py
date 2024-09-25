import pandas as pd
from openpyxl import Workbook
from datetime import datetime

# 可配置变量
# Excel文件路径--现有未涂色的文件
file_path = r'C:\Users\JA085914\Desktop\PY\画图\树状结构清单.xlsx'

# 新生成的Excel文件路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 生成时间戳，格式为：年月日_时分秒
new_file_path = fr'C:\Users\JA085914\Desktop\PY\画图\xmind导入_{timestamp}.xlsx'

# 需要读取的列名称
# 注意：列名称必须与Excel文件中的列名称完全一致
# 从前到后代表1~6级索引
column_names = ["高压进线", "高压柜(1)", "变压器（2）", "电表号（3）", "回路号（4）", "备注"]

# 读取数据并设置多级索引
df = pd.read_excel(file_path, usecols=column_names)
df.set_index(column_names, inplace=True)

# 创建新Excel文档
wb = Workbook()
ws = wb.active

# 写入列标题
ws.append(column_names)

# 用于跟踪上一次写入索引的位置
last_written_level = [-1] * len(df.index.names)

# 遍历多级索引
for index_tuple in df.index.unique():
    for level in range(len(index_tuple)):
        # 确保每个级别的新条目写在父索引的下一行
        if last_written_level[level] != index_tuple[level]:
            ws.append([''] * level + [index_tuple[level]])
            last_written_level[level] = index_tuple[level]

# 保存新的Excel文件
wb.save(new_file_path)
print(f"新文件已保存: {new_file_path}")
