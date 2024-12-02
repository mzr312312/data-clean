import os
import requests
import pandas as pd
from datetime import datetime
import json

# 设置请求的 URL
url = 'http://10.86.6.3:8081/japrojecttag/timeseries'

tagCodes = [
    "SJ-B-23-1-Efp-0001_AE01_F",
    "SJ-B-23-1-Efp-0002_AE01_F",
    "SJ-B-23-1-Efp-0003_AE01_F",
    "SJ-B-23-1-Efp-0004_AE01_F",
    "SJ-B-23-1-Efp-0005_AE01_F",
    "SJ-B-23-1-Efp-0006_AE01_F",
    "SJ-B-23-1-Efp-0007_AE01_F",
    "SJ-B-23-1-Efp-0008_AE01_F",
    "SJ-B-23-1-Efp-0009_AE01_F",
    "SJ-B-23-1-Efp-0010_AE01_F",
    "SJ-B-23-1-Efp-0011_AE01_F",
    "SJ-B-23-1-Efp-0012_AE01_F",
    "SJ-B-23-1-Efp-0013_AE01_F",
    "SJ-B-23-1-Efp-0014_AE01_F",
    "SJ-A-23-1-Efp-0001_AE01_F",
    "SJ-A-23-1-Efp-0002_AE01_F",
    "SJ-A-23-1-Efp-0003_AE01_F",
    "SJ-T-23-1-Efp-0001_AE01_F",
    "SJ-T-23-1-Efp-0002_AE01_F",
    "SJ-T-23-1-Efp-0003_AE01_F",
    "SJ-T-23-1-Efp-0004_AE01_F",
    "SJ-T-23-1-Efp-0005_AE01_F",
    "SJ-T-23-1-Efp-0006_AE01_F",
    "SJ-T-23-1-Efp-0007_AE01_F",
]
# 设置时间范围
start_time = "2024-11-20 00:00:00"
end_time = "2024-11-22 00:00:00"
granularity_minutes = 10
# 用于存储所有 DataFrame 的列表
all_data_frames = []


# 处理 tagValue 列的转换函数，将布尔值转换为 1 或 0，将数值转换为浮点数
def convert_tag_value(value):
    if isinstance(value, str):
        # 尝试将字符串转换为浮点数，如果成功则返回该浮点数
        try:
            return float(value)
        except ValueError:
            # 如果转换失败，继续判断是否为布尔值
            if value.lower() == 'true':
                return 1
            elif value.lower() == 'false':
                return 0
            else:
                return None  # 或者可以返回一个默认值，如 0

    elif isinstance(value, bool):
        return 1 if value else 0

    return float(value)  # 默认将其他情况转换为 float


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
    print(response)
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
                # 使用转换函数处理 tagValue 列（如果是布尔值，则转换为 1 或 0，如果是数值，则转换为浮点数）
                df['tagValue'] = df['tagValue'].apply(convert_tag_value)  # 使用自定义函数处理 tagValue
                # 转换 time 列为 datetime
                df['time'] = pd.to_datetime(df['time'])
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
                # if 'tagvalue' in df.columns:
                #     df['tagvalue'] = pd.to_numeric(df['tagvalue'], errors='coerce')  # 转换为数值类型

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
    combined_df.to_excel("conmbined1.xlsx")
    # 验证 tagValue 列的每个值是否为 float
    is_float = combined_df['tagValue'].apply(lambda x: isinstance(x, float))
    # 把combined_df保存到excel文件
    # combined_df.to_excel("combined.xlsx")
    # 打印非 float 的值
    not_float_values = combined_df.loc[~is_float, 'tagValue']
    print("不是 float 的值有：")
    print(not_float_values)
else:
    print("没有可合并的数据。")
    combined_df = pd.DataFrame()  # 为了后续代码安全，初始化为空的DataFrame

# 1）按照 tagCode 列和 time 列升序排列
combined_df.sort_values(by=['tagCode', 'time'], inplace=True)

# 2）使用 floor 方法，精确到分钟
if not combined_df.empty:
    combined_df['time'] = combined_df['time'].dt.floor('min')

# 3) 使用pandas的groupby和resample方法，按照每个tagCode的granularity_minutes的分钟粒度，删除多余的行
if not combined_df.empty:
    # 设置时间列为索引
    combined_df.set_index('time', inplace=True)

    # 按tagCode分组并重新采样
    combined_cut_df = (combined_df.groupby('tagCode')
                       .resample(f'{granularity_minutes}min')
                       .first()
                       .droplevel(0))  # 移除最外层的索引（即tagCode），仅保留时间索引

    # 重置索引，将'time'转回列
    combined_cut_df.reset_index(inplace=True)

    print("combined_cut_df=\n", combined_cut_df)

# 4) 在combined_cut_df的基础上，计算每granularity_minutes分钟的差值diff，并添加到combined_cut_df的新列diff
combined_cut_df['diff'] = combined_cut_df.groupby('tagCode')['tagValue'].diff()

print("combined_cut_df after diff calculation=\n", combined_cut_df)

# 5）利用fillna方法填充第一行的NaN值
combined_cut_df.bfill(inplace=True)
print("final combined_cut_df=\n", combined_cut_df)

# 获取当前时间戳
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 定义输出文件的路径
output_file_path = f"../../PY/时序数据处理/按颗粒度{granularity_minutes}min筛选的原始数据_{current_timestamp}.xlsx"
# 保存DataFrame
combined_cut_df.to_pickle('combined_cut_df.pkl')

# 保存结果到 Excel 文件
combined_cut_df.to_excel(output_file_path)
print(f"结果已保存到: {output_file_path}")


# 在计算diff值之后，定义diff_values字典
diff_values = {}

# 遍历combined_cut_df，填充diff_values字典
for index, row in combined_cut_df.iterrows():
    tag_code = row['tagCode']
    timestamp = row['time'].strftime('%Y-%m-%d %H:%M:%S')  # 将时间转换为字符串
    diff_value = row['diff']

    # 确保tagCode在字典中
    if tag_code not in diff_values:
        diff_values[tag_code] = {}

    # 将diff值添加到时间戳的字典中
    diff_values[tag_code][timestamp] = diff_value

# 转换为JSON格式
diff_values_json = json.dumps(diff_values, ensure_ascii=False)
# 保存为txt文件
with open('diff_values.txt', 'w', encoding='utf-8') as f:
    f.write(diff_values_json)
# 输出JSON格式的diff_values
print("diff_values (JSON格式):", diff_values_json)

# 下面可以将diff_values_json作为接口传递给其他模块
