import pandas as pd
from datetime import datetime
import os

# 使用说明：
# 1）指定需要读取的数据源Excel文件的完整路径
# 2）指定写入新标签页的文件名和路径（底部）
# 3）指定读取Excel文件中"设备类型清单"和"数据点清单"时的读取列（A列是0，B列是1，以此类推）
# 4）指定读取Excel文件中"设备类型清单"和"数据点清单"中各列的名称（例如，usecols=[1, 5]对应['设备/仪表原有编号', '设备类型']），这些名称后面都要写入新文件，作为列标题
# 5）注意第18行和第22行，也要对应表格标题修改
# 5）确定header（等于0代表第一行是标题列）

# 功能说明
# 使用了pandas库的merge功能，左对齐（左就是df_equipment这张表，表示保留了全部的设备类型清单中的全部的设备名称，即使该名称没有数据点清单中的数据点支持，也会写入NA值）。

# 以下为正式代码

# 指定需要读取数据的Excel文件的完整路径
excel_file_path = r"C:\Users\JA085914\Desktop\PY\数据处理\01.合并数据表.xlsx"

# 读取Excel文件
with pd.ExcelFile(excel_file_path) as xls:
    # 读取“设备类型清单”
    df_equipment = pd.read_excel(xls, sheet_name="设备类型清单", usecols=[0, 4], header=0) #A列是0，B列是1，以此类推
    df_equipment.columns = ['设备/仪表原有编号（点表）', '设备类型']

    # 读取“数据点清单”，共读取4列
    df_points = pd.read_excel(xls, sheet_name="数据点清单", usecols=[1, 2, 8], header=0) #A列是0，B列是1，以此类推
    df_points.columns = ['设备类型', '采集点特征字段','数据点后缀', ]  # 添加一个临时列名，用于后续处理

# 将设备类型转换为一致的格式以便匹配
df_equipment['设备类型'] = df_equipment['设备类型'].str.strip()
df_points['设备类型'] = df_points['设备类型'].str.strip()

# 重新排序df_points的列，将"数据点名"移到最前面
df_points = df_points[['数据点后缀', '设备类型', '采集点特征字段']]

# 合并数据
merged_df = pd.merge(df_equipment, df_points, on='设备类型', how='left')
# 获取 excel_file_path 的目录
excel_file_dir = os.path.dirname(excel_file_path)
# 写入新标签页
# 生成 output_file_path
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = os.path.join(excel_file_dir, f"合并_{timestamp}.xlsx")

# 写入新标签页
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    merged_df.to_excel(writer, sheet_name="汇总", index=False)

print("数据已成功合并并保存到'汇总'标签页。")