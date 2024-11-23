"""
该脚本用于从指定的 API 接口依次获取多个数据点的时间序列数据，并将其合并为一个 Excel 文件。

使用方法：
1. 更改 `url` 变量的值为实际的 API 接口地址。
2. 根据需要更新 `tagCodes` 列表，添加或移除要查询的 `tagCode`。
3. 设置时间范围，确保 `start_time` 和 `end_time` 的值为所需查询的时间段。
4. 运行脚本，数据将被获取并合并为一个文件，保存路径在代码中指定。

输出结果：
- 该脚本将在 `../../PY/时序数据处理/` 目录中生成一个 Excel 文件，文件名格式为 `合并数据_YYYYMMDD_HHMMSS.xlsx`，其中 `YYYYMMDD_HHMMSS` 为当前时间戳。
- Excel 文件包含时间拆分后的年、月、日、时、分列，及每条数据对应的 `tagCode` 以及 `tagvalue`。

注意事项：
- 确保在运行脚本之前安装所需的库，您可以使用以下命令进行安装：

pip install requests pandas openpyxl

- 脚本中假定 API 的返回数据中包含 `timeseries` 键，并且存在 `time` 和 `tagvalue` 字段，确保您了解 API 响应的结构。
- 如果在获取数据时遇到任何警告或错误信息，请检查 `tagCode` 和时间范围是否正确。

作者： 马卓然
版本： 1.0
创建日期： 2024年11月22日
"""

import os
import requests
import pandas as pd
from datetime import datetime

# 设置请求的 URL
url = 'http://10.86.6.3:8081/japrojecttag/timeseries'

tagCodes = [
    'SJ-T-23-1-Efp-0001_AE01_F',
    'SJ-T-23-1-Efp-0002_AE01_F',
    'SJ-T-23-1-Efp-0003_AE01_F',
    'SJ-T-23-1-Efp-0004_AE01_F',
    'SJ-T-23-1-Efp-0005_AE01_F',
    'SJ-T-23-1-Efp-0006_AE01_F',
    'SJ-T-23-1-Efp-0007_AE01_F',
]

# 设置时间范围
start_time = "2024-11-19 09:45:00"
end_time = "2024-11-19 11:30:00"
granularity_minutes = 5
# 用于存储所有 DataFrame 的列表
all_data_frames = []

# 遍历每个 tagCode
for tagCode in tagCodes:
    # 设置请求的数据
    data = {
        "tagCode": tagCode,
        "startTime": start_time,
        "endTime": end_time
    }

    # 发送 POST 请求
    response = requests.post(url, json=data)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 数据
        json_data = response.json()

        # 检查 'data' 和 'timeseries' 是否存在
        if json_data and 'data' in json_data and json_data['data'] is not None:
            timeseries_data = json_data['data'].get('timeseries')

            # 确保 timeseries_data 不是 None
            if timeseries_data is not None:
                # 将数据转换为 DataFrame
                df = pd.DataFrame(timeseries_data)
                # 转换 tagValue 列为 float
                df['tagValue'] = df['tagValue'].astype(float)
                # 添加 tagCode 列
                df['tagCode'] = tagCode

                # 如果有时间列，进行拆分
                if 'time' in df.columns:
                    df['time'] = pd.to_datetime(df['time'])  # 转换时间为时间格式
                    df['年'] = df['time'].dt.year
                    df['月'] = df['time'].dt.month
                    df['日'] = df['time'].dt.day
                    df['时'] = df['time'].dt.hour
                    df['分'] = df['time'].dt.minute

                # 转换 tagvalue 为数字类型
                if 'tagvalue' in df.columns:
                    df['tagvalue'] = pd.to_numeric(df['tagvalue'], errors='coerce')  # 转换为数值类型

                # 添加到总的 DataFrame 列表中
                all_data_frames.append(df)
            else:
                print(f"警告: tagCode {tagCode} 的 timeseries 数据为空。")
        else:
            print(f"警告: tagCode {tagCode} 的响应格式不正确或数据为空。")
    else:
        print(f"请求失败，状态码: {response.status_code}, 响应：{response.text}")

# 合并所有 DataFrame
if all_data_frames:
    combined_df = pd.concat(all_data_frames, ignore_index=True)
    # combined_df.to_excel("conmbined1.xlsx")
    # 验证 tagValue 列的每个值是否为 float
    is_float = combined_df['tagValue'].apply(lambda x: isinstance(x, float))

    # 打印非 float 的值
    not_float_values = combined_df.loc[~is_float, 'tagValue']
    print("不是 float 的值有：")
    print(not_float_values)
else:
    print("没有可合并的数据。")
    combined_df = pd.DataFrame()  # 为了后续代码安全，初始化为空的DataFrame



# 1）按照 tagCode 列和 time 列升序排列
combined_df.sort_values(by=['tagCode', 'time'], inplace=True)
# combined_df.to_excel("conmbined2.xlsx")

# 2）使用 floor 方法，精确到分钟
if not combined_df.empty:
    combined_df['time'] = combined_df['time'].dt.floor('min')

# 3）创建一个combined_df的独立副本，用于后续存储删除行后的表格
combined_cut_df = combined_df.copy()
print("combined_df=\n", combined_df)

# 4）按照时间间隔，删除指定时间间隔内的重复数据的行
# 遍历每一行，计算其与前一行的时间差
print(len(combined_cut_df))

# 初始化一个新的 DataFrame 用于保存保留的行
result_df = pd.DataFrame(columns=combined_cut_df.columns)

# 将第一行直接加入到结果 DataFrame 中
if not combined_cut_df.empty:
    result_df = pd.concat([result_df, combined_cut_df.iloc[[0]]], ignore_index=True)

for i in range(1, len(combined_cut_df)):
    # 计算当前行时间与前一行的时间差
    time_diff = (combined_cut_df.iloc[i]['time'] - combined_cut_df.iloc[i - 1]['time']).total_seconds() / 60
    print(f"第 {i} 行，时间差为 {time_diff} 分钟")
    # 如果时间差小于 granularity_minutes，则删除当前行（不做添加）
    if time_diff >= granularity_minutes:
        result_df = pd.concat([result_df, combined_cut_df.iloc[[i]]], ignore_index=True)

# 打印结果
print("result_df=\n", result_df)
result_df.to_excel("result_df.xlsx")
# 有问题，只剩一行了，还得检查为什么不添加，输出里打印了当前的时间差，可以看到都是0,1分钟这样的，应该是因为时间差小于granularity_minutes，所以就不添加了，所以最后只剩一行了
# 肯定不对，因为时间差都是0或者1分钟，还得换逻辑，应该是如果i行和第i-1的时间差小于granularity_minutes，则继续查找下一行，下一行应该还和第最开始的那个i-1行做对比，直到某一行和第i行的时间差大于等于granularity_minutes，然后把第i行加入结果DataFrame