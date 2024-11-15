import pandas as pd
from datetime import datetime

"""
本脚本用于统计 Excel 文件中指定列的各个值的重复次数，并将统计结果保存到新的 Excel 文件中。

使用说明：
1. 确保安装了 pandas 库，如果尚未安装，可以使用命令 `pip install pandas` 来安装。
2. 将你要统计的 Excel 文件路径和文件名更新到 `input_file_path` 变量中。
3. 确认要统计的数据所在的工作表名称，并更新 `sheet_name` 变量。
4. 在 `column_name` 变量中填入你要统计的列的名称（注意是列名，不是索引号）。
5. 运行脚本后，程序会读取指定的 Excel 文件，统计该列中每个值出现的次数，并将结果保存为一个新的 Excel 文件。
6. 新文件将保存在与原文件相同的目录中，文件名将包含当前的时间戳以避免重名。

输出：
脚本运行成功后，会在控制台输出“已执行成功，请查看新文件”，并在指定路径生成一个新的 Excel 文件，其中包含两列：'列的内容' 和 '出现次数'。

注意：请确保输入的文件路径和列名的准确性以避免运行错误。
"""





# 引入时间模块，用于生成文件名
# 定义变量
# 定义读取的数据源文件路径
input_file_path = r'../../PY/数据处理/04.统计某一列所有值的重复次数-模板.xlsx'
# 定义该数据原文件里的tab页名称
sheet_name = '统计'
# 定义该tab页里，要统计哪一列的数据（直接输入列的名字，不需要数是第几列）
column_name = '需要统计的文字'
# 定义输出的新文件的路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = rf'../../PY/数据处理/统计结果_{timestamp}.xlsx'
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