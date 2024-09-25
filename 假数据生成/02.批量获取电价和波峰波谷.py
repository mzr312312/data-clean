import pandas as pd

# 文件路径
file1_path = 'E:/工作/2.方案设计/2 数采工作/1 各基地/01 石家庄基地/2 石家庄梳理成果/01.配电系统/给开发组的各种人造数据/新数据生成.xlsx'
file2_path = 'E:/工作/2.方案设计/2 数采工作/1 各基地/01 石家庄基地/2 石家庄梳理成果/01.配电系统/给开发组的各种人造数据/fact_electricity_price.xlsx'

# 读取文件1
# 在读取数据时，确保合适的数据类型
df1 = pd.read_excel(file1_path, sheet_name='数据', dtype={'time_period': object})


# 读取文件2
df2 = pd.read_excel(file2_path, sheet_name='电价')


# 解析consumption_time_id为日期时间
def parse_consumption_time_id(time_id):
    # 确保time_id是字符串
    time_id = str(time_id)

    # 检查时间ID的长度是否正确
    if len(time_id) != 11 or not time_id.startswith('6'):
        raise ValueError(f"Invalid consumption_time_id format: {time_id}")

    # 假设time_id格式如描述，去除前缀'6'
    date_str = time_id[1:9]
    hour_str = time_id[9:11]

    # 打印调试信息
    #print(f"Parsing time_id: {time_id}, date_str: {date_str}, hour_str: {hour_str}")

    # 确保hour_str是两位数
    if not hour_str.isdigit() or len(hour_str) != 2:
        raise ValueError(f"Invalid hour string: {hour_str}")

    # 将hour_str转换为整数
    hour = int(hour_str)

    # 处理小时数为24的情况
    if hour == 24:
        hour = 0
        next_day = pd.to_datetime(date_str) + pd.Timedelta(days=1)
        date_str = next_day.strftime('%Y%m%d')

    # 创建开始时间
    start_time = pd.to_datetime(f"{date_str} {hour:02d}:00:00")

    # 计算结束时间
    end_time = pd.to_datetime(f"{date_str} {(hour + 1) % 24:02d}:00:00")

    return start_time, end_time


# 遍历文件1中的每一行
for index, row in df1.iterrows():
    base_id = row['base_id']
    consumption_time_id = row['consumption_time_id']

    try:
        start_time, end_time = parse_consumption_time_id(consumption_time_id)
    except ValueError as e:
        print(e)
        continue

    # 在文件2中查找匹配项
    match = df2[(df2['base_id'] == base_id) &
                (df2['start_time'] <= start_time) &
                (df2['end_time'] >= end_time)]

    if not match.empty:
        df1.at[index, 'time_period'] = match.iloc[0]['time_period']
        df1.at[index, '单价'] = match.iloc[0]['price']

# 将结果保存回文件1
with pd.ExcelWriter(file1_path, mode='a', if_sheet_exists='overlay') as writer:
    df1.to_excel(writer, index=False, sheet_name='数据', startrow=1, header=None)

print("处理完成，文件已保存。")