import pandas as pd
import re
from datetime import datetime

"""
该脚本用于读取一个Excel文件中的特定列，按照文本和数字的真正顺序进行排序，并将排序后的结果保存为一个新的Excel文件。

使用说明：
1. 确保已安装 pandas 库和 openpyxl 库，使用以下命令安装：
   pip install pandas openpyxl

2. 修改以下变量以适应你的文件路径和列名：
   - input_file_path: 输入Excel文件的相对路径。
   - column_name: 需要排序的列的名称。

3. 运行脚本，程序会读取指定的Excel文件，对指定列的内容进行排序，并将结果保存到当前路径下，文件名包含当前时间戳，以避免覆盖。

排序规则：
- 本脚本采用自然排序算法，处理数据中的文本与数字组合，例如：
  - "气动阀10" 会排在 "气动阀2" 的后面，符合人类的直觉排序方式。

输出：
- 脚本执行完成后，将生成一个名为“真正生序排列_时间戳.xlsx”的文件，包含排序后的数据。
- 会有报错提示，但不影响程序运行。  
"""


# 定义一个函数，使用正则表达式将字符串分割为文本和数字的组合，最终返回一个列表，用于排序时的比较。
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# 读取Excel文件
input_file_path = r'../../PY/数据处理/21.把“文本+数字”的一列内容按照真正的顺序排列.xlsx'
df = pd.read_excel(input_file_path)

# 假设“需要排列的内容”为数据帧的列名
column_name = '需要排列的内容'

# 对该列进行排序
df_sorted = df.sort_values(by=column_name, key=lambda col: col.map(natural_sort_key))

# 生成时间戳
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 保存为新的Excel文件
output_file_path = f'../../PY/数据处理/真正升序排列_{timestamp}.xlsx'
df_sorted.to_excel(output_file_path, index=False)

print(f"排序完成，文件已保存至：{output_file_path}")
