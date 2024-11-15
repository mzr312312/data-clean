import pandas as pd
from openpyxl import Workbook
from datetime import datetime
# 说明：
# 此脚本用于给一列数据点编码，按照色块，依次编号的功能，目的是用于数据点编码清单的编写
# 我需要在源文件中填写一列（不要修改列名，否则认不出来），如下面的第一列
# 填写的列需要带有色块（按设备类型分类的）
# 这样，系统会识别色块，明确每个设备类型下，有哪些重复的，或不重复的数据点编码
# 然后系统会给这些数据点编码一个数字编号，重复的话就1,2,3,4以此类推，不重复则从1重新开始
# 注意：我填写的列，最好按照数据点编码（第一列）先排个序，但注意不要破坏色块的结构
# 以下是一个示例，所有行的内容属于同一个色块
# AE	1
# AN	1
# AN	2
# AN	3
# AN	4
# AN	5
# AN	6
# AN	7
# AN	8
# AN	9
# CR	1
# CR	2
# CR	3
# CR	4
# PF	1
# PW	1

# 文件路径
file_path = r'C:\Users\JA085914\Desktop\PY\数据处理\19.按交替涂色的色块，自动给信号编码排序.xlsx'
# 新生成的文件路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
new_file_path = fr'C:\Users\JA085914\Desktop\PY\数据处理\数据点编号_{timestamp}.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

# 涉及的列
target_column = '把要编序号的内容放在这里'

# 存储结果的列表
results = []
current_block = []
previous_value = None

# 遍历目标列，识别色块
for value in df[target_column]:
    if value == previous_value:
        current_block.append(value)  # 如果相同，继续添加到当前色块
    else:
        # 当前值与前一个值不同，处理当前色块
        if current_block:
            # 为当前色块编号
            count_map = {}
            for item in current_block:
                if item in count_map:
                    count_map[item] += 1
                else:
                    count_map[item] = 1
                results.append((item, count_map[item]))

        # 开启新的色块
        current_block = [value]

    previous_value = value

# 处理最后一个色块
if current_block:
    count_map = {}
    for item in current_block:
        if item in count_map:
            count_map[item] += 1
        else:
            count_map[item] = 1
        results.append((item, count_map[item]))

# 创建新的工作簿
wb = Workbook()
ws = wb.active

# 写入标题
ws.append(['原始内容', '编号'])

# 写入结果
for original_value, number in results:
    ws.append([original_value, number])

# 保存新的文件
wb.save(new_file_path)

print(f"新的文件已生成：{new_file_path}")


