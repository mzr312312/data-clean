import pandas as pd
from datetime import datetime, timedelta
import os

# 定义文件路径
file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\2 石家庄梳理成果\01.配电系统\给开发组的各种人造数据\[模板]fact_consumption_bas_equipment_hourly_202409181350.xlsx'  # 修改为实际文件路径
output_folder = os.path.dirname(file_path)

# 尝试读取 Excel 文件
try:
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"读取文件时出错: {e}")
    df = pd.DataFrame()  # 如果读取失败，创建一个空的 DataFrame

# 删除原有的consumption_time_id列，如果存在的话
if 'consumption_time_id' in df.columns:
    del df['consumption_time_id']


# 生成时间序列
def generate_time_series(start_date, end_date):
    start = datetime.strptime(start_date, '%Y.%m.%d')
    end = datetime.strptime(end_date, '%Y.%m.%d')
    time_series = []
    current = start
    while current <= end:
        for hour in range(1, 25):
            time_series.append(f"6{current.strftime('%Y%m%d')}{hour:02}")
        current += timedelta(days=1)
    return time_series

# 生成两个时间段的时间序列
time_series_2023 = generate_time_series('2023.1.1', '2023.3.31')
time_series_2024 = generate_time_series('2024.1.1', '2024.3.31')
time_series = time_series_2023 + time_series_2024

# 扩展DataFrame
expanded_rows = []
for _, row in df.iterrows():
    for time_id in time_series:
        new_row = row.copy()
        new_row['consumption_time_id'] = time_id
        expanded_rows.append(new_row)

expanded_df = pd.DataFrame(expanded_rows)

# 保存新的CSV文件
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
output_file_name = f'新生成数据{timestamp}.csv'
output_file_path = os.path.join(output_folder, output_file_name)
expanded_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"新文件已保存至: {output_file_path}")