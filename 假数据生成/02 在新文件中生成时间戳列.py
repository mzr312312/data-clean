import openpyxl
from datetime import datetime, timedelta

# 创建Excel文档
file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\2 石家庄梳理成果\01.配电系统\给开发组的各种人造数据\假数据（第二批0925）\时间戳.xlsx'
wb = openpyxl.Workbook()
ws = wb.active

# 定义开始和结束日期
start_date_2023 = datetime(2023, 1, 1)
end_date_2023 = datetime(2023, 3, 31)
start_date_2024 = datetime(2024, 1, 1)
end_date_2024 = datetime(2024, 3, 31)

# 函数：生成时间戳格式
# 函数：生成时间戳格式
def generate_timestamp(date, hour):
    year = str(date.year)[2:]  # 取年份最后两位
    month = str(date.month).zfill(2)  # 月份，补零
    day = str(date.day).zfill(2)  # 日期，补零
    hour = str(hour + 1).zfill(2)  # 小时，加1后补零
    return f"620{year}{month}{day}{hour}"  # 修改为620XXXX格式

# 生成时间戳并写入Excel
row = 1
for date in [start_date_2023, start_date_2024]:
    end_date = end_date_2023 if date.year == 2023 else end_date_2024
    current_date = date
    while current_date <= end_date:
        for hour in range(24):  # 从0到23生成小时，实际显示从01到24
            timestamp = generate_timestamp(current_date, hour)
            ws.cell(row=row, column=1, value=timestamp)
            row += 1
        current_date += timedelta(days=1)  # 前往下一天
# 保存Excel文档
wb.save(file_path)
print(f"时间戳已生成并保存到 {file_path}")