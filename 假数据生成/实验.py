import pandas as pd

# 读取CSV文件
file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\2 石家庄梳理成果\01.配电系统\给开发组的各种人造数据\fact_electricity_price_20240918.csv'

# 加载CSV文件，指定编码格式
data = pd.read_csv(file_path, encoding='gbk')  # 或者尝试 'latin1'

# 遍历每一行并打印格式化的日期和时间
for index, row in data.iterrows():
    start_time = pd.to_datetime(row['start_time'])
    end_time = pd.to_datetime(row['end_time'])

    print(f"开始时间：{start_time.year}年{start_time.month}月{start_time.day}日，"
          f"{start_time.hour}时{start_time.minute}分{start_time.second}秒")
    print(f"结束时间：{end_time.year}年{end_time.month}月{end_time.day}日，"
          f"{end_time.hour}时{end_time.minute}分{end_time.second}秒")
