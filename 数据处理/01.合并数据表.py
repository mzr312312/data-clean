import pandas as pd
from datetime import datetime
import os
import openpyxl


# 指定需要读取数据的Excel文件的完整路径
excel_file_path = rf"../PY/数据处理/01.合并数据表.xlsx"

# 读取Excel文件
with pd.ExcelFile(excel_file_path, engine='openpyxl') as xls:
    # 读取“设备类型清单”，直接读取所需的列，并保持原列名
    df_equipment = pd.read_excel(xls, sheet_name="设备类型清单", usecols=['设备/仪表原有编号（点表）', '设备类型'])  # 直接使用列名

    # 读取“数据点清单”，直接读取所需的列，并保持原列名
    df_points = pd.read_excel(xls, sheet_name="数据点清单", usecols=['设备类型', '采集点特征字段', '数据点后缀'])  # 直接使用列名

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
