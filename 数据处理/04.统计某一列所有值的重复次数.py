import pandas as pd
from datetime import datetime
# 引入时间模块，用于生成文件名
# 定义变量
# 定义读取的数据源文件路径
input_file_path = r'C:\Users\JA085914\Desktop\PY\数据处理\04.统计某一列所有值的重复次数-模板.xlsx'
# 定义该数据原文件里的tab页名称
sheet_name = '统计'
# 定义该tab页里，要统计哪一列的数据（直接输入列的名字，不需要数是第几列）
column_name = '需要统计的文字'
# 定义输出的新文件的路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = rf'C:\Users\JA085914\Desktop\PY\数据处理\统计结果_{timestamp}.xlsx'
# 定义输出的新文件里，两列的名字是什么。此处，第一列代表"需要统计的那一列中的所有内容，去重后的结果", 第二列代表"这些内容出现的次数"
output_column_names = ['列的内容', '出现次数']

# 读取 Excel 文件
df = pd.read_excel(input_file_path, sheet_name=sheet_name, usecols=[column_name])

# 统计每种字母出现的次数
letter_counts = df[column_name].value_counts().reset_index()

# 重命名列名
letter_counts.columns = output_column_names

# 将结果保存到新的 Excel 文件
letter_counts.to_excel(output_file_path, index=False)

print("已执行成功，请查看新文件")