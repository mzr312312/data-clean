import requests
import pandas as pd
from datetime import datetime

# 设置请求的 URL
url = 'http://10.86.6.3:8081/japrojecttag/timeseries'  # 替换为实际的 API 地址

# 设置要查询的 tagCode 列表
tag_codes = [
    "SJ-B-14-QDVZ-FQ-0002_FR01_F",
    "SJ-A-14-QDVZ-FQ-0008_FR01_F",
    "SJ-A-14-QDVZ-FQ-0009_FR01_F",
    "SJ-A-14-QDVZ-FQ-0010_FR01_F",
    "SJ-A-14-QDVZ-FQ-0011_FR01_F",
    "SJ-A-14-QDVZ-FQ-0014_FR01_F",
    "SJ-X-14-QDVZ-FQ-0018_FR01_F",
    "SJ-T-14-QDVZ-FQ-0001_FR01_F",
    "SJ-B-14-QDVZ-FQ-0004_FR01_F",
    "SJ-T-14-QDVZ-FQ-0005_FR01_F",
    "SJ-QT-14-QDVZ-FQ-0006_FR01_F",
    "SJ-T-14-QDVZ-FQ-0007_FR01_F",
    "SJ-A-14-QDVZ-FQ-0013_FR01_F",
    "SJ-QT-14-QDVZ-FQ-0015_FR01_F",
    "SJ-X-14-QDVZ-FQ-0017_FR01_F",
]

# 设置时间范围
start_time = "2024-11-22 04:00:00"
end_time = "2024-11-22 12:00:00"

# 用于存储所有 DataFrame 的列表
all_data_frames = []

# 遍历每个 tagCode
for tag_code in tag_codes:
    # 设置请求的数据
    data = {
        "tagCode": tag_code,
        "startTime": start_time,
        "endTime": end_time
    }

    # 发送 POST 请求
    response = requests.post(url, json=data)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 数据
        json_data = response.json()

        # 打印响应内容以进行调试
        print(f"tagCode: {tag_code}, 响应数据: {json_data}")

        # 检查 'data' 和 'timeseries' 是否存在
        if json_data and 'data' in json_data and json_data['data'] is not None:
            timeseries_data = json_data['data'].get('timeseries')

            # 确保 timeseries_data 不是 None
            if timeseries_data is not None:
                # 将数据转换为 DataFrame
                df = pd.DataFrame(timeseries_data)

                # 添加 tagCode 列
                df['tagCode'] = tag_code

                # 如果有时间列，进行拆分
                if 'time' in df.columns:
                    df['时间'] = pd.to_datetime(df['time'])  # 假设时间列名为 'time'
                    df['年'] = df['时间'].dt.year
                    df['月'] = df['时间'].dt.month
                    df['日'] = df['时间'].dt.day
                    df['时'] = df['时间'].dt.hour
                    df['分'] = df['时间'].dt.minute

                    # 移除原来的时间列
                    df.drop(columns=['时间'], inplace=True)

                # 调整列顺序，将 tagCode 和 tagValue 移动到最后
                if 'tagValue' in df.columns:  # 假设 tagValue 列名为 'tagValue'
                    # 重新排列列顺序
                    cols = [col for col in df.columns if col not in ['tagValue', 'tagCode']]
                    df = df[cols + ['tagCode', 'tagValue']]

                # 添加到总的 DataFrame 列表中
                all_data_frames.append(df)
            else:
                print(f"警告: tagCode {tag_code} 的 timeseries 数据为空。")
        else:
            print(f"警告: tagCode {tag_code} 的响应格式不正确或数据为空。")
    else:
        print(f"请求失败，状态码: {response.status_code}, 响应：{response.text}")

# 合并所有 DataFrame
if all_data_frames:
    combined_df = pd.concat(all_data_frames, ignore_index=True)

    # 导出为一个 Excel 文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'../../PY/时序数据处理/合并数据_{timestamp}.xlsx'
    combined_df.to_excel(output_file, index=False)

    print(f"所有数据已成功合并并导出到 {output_file}")
else:
    print("没有可合并的数据。")
