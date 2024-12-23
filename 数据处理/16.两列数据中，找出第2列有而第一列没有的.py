import pandas as pd
from datetime import datetime

# 读取Excel文件
file_path = r'../../PY/数据处理/16.两列数据中，找出第2列有而第一列没有的.xlsx'
data = pd.read_excel(file_path)

# 假设列名是"列1"和"列2"
column1_values = set(data['列1'].astype(str).values)  # 将第一列转为字符串并转为集合
column2_values = set(data['列2'].astype(str).values)  # 将第二列转为字符串并转为集合

# 查找列2有而列1没有的内容
difference = column2_values - column1_values

# 将结果转换为DataFrame
result_df = pd.DataFrame(list(difference), columns=['列2有而列1没有'])

# 生成当前时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = fr'../../PY/数据处理/对比_{timestamp}.xlsx'

# 输出结果到新的Excel文件
result_df.to_excel(output_file_path, index=False)

print(f'输出文件已保存至: {output_file_path}')
