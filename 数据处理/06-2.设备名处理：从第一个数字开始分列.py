import pandas as pd
import re
from datetime import datetime

# 文件路径
input_file_path = r'D:\PycharmProjects\PY\数据处理\06.设备名处理：从第一个数字开始分列.xlsx'
sheet_name = '分列'
original_column_name = '把需要分列的内容粘在下面'

# 读取Excel文件
df = pd.read_excel(input_file_path, sheet_name=sheet_name)

# 定义一个函数，用来分割字符串
def split_string(s):
    # 使用正则表达式找到第一个数字出现的位置
    match = re.search(r'\d', s)
    if match:
        index = match.start()
        # 分割字符串
        part1 = s[:index].strip()  # 去除可能的空格
        part2 = s[index:].strip()   # 去除可能的空格
        return part1, part2
    else:
        # 如果没有数字，则返回原字符串和空字符串
        return s.strip(), ''

# 应用函数到DataFrame的指定列
df[['分列1', '分列2']] = df[original_column_name].apply(
    lambda x: pd.Series(split_string(x))
)

# 重命名原始列名为“分列前”
df.rename(columns={original_column_name: '分列前'}, inplace=True)

# 获取当前时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 创建输出文件路径，包含时间戳
output_dir = input_file_path.rsplit('\\', 1)[0]  # 获取输入文件所在的目录
output_file_name = f'分列_{timestamp}.xlsx'
output_file_path = f'{output_dir}\\{output_file_name}'

# 将结果保存到新的Excel文件
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='分列后的内容', index=False)

print(f"处理完成并已保存至 {output_file_path}！")