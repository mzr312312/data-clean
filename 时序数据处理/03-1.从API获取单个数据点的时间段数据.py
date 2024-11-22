import requests
import pandas as pd
from datetime import datetime

# 设置请求的 URL
url = 'http://10.86.6.3:8081/japrojecttag/timeseries'  # 替换为实际的 API 地址

# 设置请求的数据（根据你的 API 需求进行调整）
data = {
    "tagCode":"SJ-B-14-QDVZ-FQ-0002_FR01_F",
    "startTime":"2024-11-22 10:00:00",
    "endTime":"2024-11-22 14:00:00"
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 检查请求是否成功
if response.status_code == 200:
    # 解析 JSON 数据
    json_data = response.json()

    # 提取 timeseries 数据
    timeseries_data = json_data['data']['timeseries']

    # 将数据转换为 DataFrame
    df = pd.DataFrame(timeseries_data)

    # 创建时间戳字符串，格式为 YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 导出为 Excel 文件，并在文件名中添加时间戳
    output_file = f'../../PY/时序数据处理/单个数据点的分钟级数据_{timestamp}.xlsx'  # Excel 文件名
    df.to_excel(output_file, index=False)  # 不包含行索引

    print(f"数据已成功导出到 {output_file}")
else:
    print(f"请求失败，状态码: {response.status_code}, 响应：{response.text}")
