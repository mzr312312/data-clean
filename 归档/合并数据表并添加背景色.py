import pandas as pd

# 指定Excel文件的完整路径
excel_file_path = "E:\\工作\\2.方案设计\\2 数采工作\\1 各基地\\01 石家庄基地\\1 石家庄梳理成果\\02 暖通空调系统\\PY实验\\【PY实验】设备清单&数据点清单（石家庄-暖通空调系统）.xlsx"

# 读取Excel文件
with pd.ExcelFile(excel_file_path) as xls:
    # 读取“设备类型清单”
    df_equipment = pd.read_excel(xls, sheet_name="设备类型清单", usecols=[1, 5], header=0)
    df_equipment.columns = ['设备/仪表原有编号', '设备类型']

    # 读取“数据点清单”
    df_points = pd.read_excel(xls, sheet_name="数据点清单", usecols=[0, 1, 33], header=0)
    df_points.columns = ['设备类型', '参数', '数据点后缀']

# 将设备类型转换为一致的格式以便匹配
df_equipment['设备类型'] = df_equipment['设备类型'].str.strip()
df_points['设备类型'] = df_points['设备类型'].str.strip()

# 合并数据
merged_df = pd.merge(df_equipment, df_points, on='设备类型', how='left')

# 添加一个新列来标记需要高亮显示的行
merged_df['Highlight'] = False
# 根据设备/仪表原有编号，每两个连续的设备号中，第一个设备号包含的所有行都涂灰色
merged_df['Highlight'] = merged_df.groupby('设备/仪表原有编号').ngroup() % 2 == 0

# 输出合并后的 DataFrame（可选）
print(merged_df.head())