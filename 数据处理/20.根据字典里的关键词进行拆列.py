import pandas as pd
import os
from datetime import datetime
"""
这个脚本用于处理Excel文件，根据预定义的关键词对特定列中的项进行拆分。

使用方法：
1. 确保输入Excel文件位于指定路径（相对路径）： "../../PY/数据处理/20.根据字典里的关键词进行拆列.xlsx"。
2. 此脚本会读取指定的列“按关键词拆列”（列名不能变，否则会报错），该列包含待处理的项。
3. 它会扫描每个项，查找预定义的关键词，并将每个项拆分为两部分：
   - 拆分点之前及最后匹配的关键词部分。
   - 拆分点之后的部分。
4. 预定义的关键词存储在列表 spilt_keyword_1 中，如果后续其他点表要梳理，可以修改此列表。
5. 如果某个项不包含任何关键词，仍会包含在输出中，但拆分后的部分会为空。
6. 处理结果将保存到一个新的Excel文件中（与源文件在同一目录下），文件名中会包含时间戳。


输出：
- 输出的Excel文件将包含三列：：
  1. '源文件项'：来自源文件的原始项。
  2. '拆分点前'：包含最后匹配关键词的项的前半部分。
  3. '拆分点后'：最后匹配关键词后的部分。

依赖库：
- pandas：请确保已安装pandas库以读取和写入Excel文件。
- openpyxl：处理Excel文件格式时需要此库。

作者：马卓然
日期：2024.11.14
"""


# 1）定义关键词列表 spilt_keyword_1
spilt_keyword_1 = [
    "BCDS", "BSGS", "BSGS1", "BSGS2", "BSGS3", "BSGS4", "BSGS5",
    "BSGS6", "CBU", "ENV1", "ENV10", "ENV11", "ENV12", "ENV13",
    "ENV14", "ENV15", "ENV16", "ENV17", "ENV2", "ENV3", "ENV4",
    "ENV5", "ENV6", "ENV7", "ENV8", "ENV9", "LLJ", "P-BOX1",
    "P-BOX2", "P-BOX3", "P-BOX4", "P-BOX5", "P-BOX6", "SYS",
    "VDB1", "VDB2", "VDB3", "VMB1", "VMB10", "VMB11", "VMB12",
    "VMB13", "VMB14", "VMB15", "VMB16", "VMB2", "VMB3", "VMB4",
    "VMB5", "VMB6", "VMB7", "VMB8", "VMB9", "WQ"
]

# 2）读取源文件，使用相对路径
source_file_path = "../../PY/数据处理/20.根据字典里的关键词进行拆列.xlsx"
df = pd.read_excel(source_file_path)

# 清洗“按关键词拆列”这一列为字符串
df['按关键词拆列'] = df['按关键词拆列'].astype(str)

# 3）遍历源文件项与列表项进行比对
split_items = []
for index, row in df.iterrows():
    item = row['按关键词拆列']

    # 找到所有关键词的索引和最后一个关键词
    found_keywords = [(keyword, item.index(keyword)) for keyword in sorted(spilt_keyword_1, key=len, reverse=True) if keyword in item]

    if found_keywords:
        # 找到靠后（最后出现的关键词）
        last_keyword, last_index = max(found_keywords, key=lambda x: x[1])

        # 拆分成前后两部分
        before_split = item[:last_index + len(last_keyword)]  # 拆分点前的内容
        after_split = item[last_index + len(last_keyword):]  # 拆分点后的内容
        split_items.append((item, before_split, after_split))  # 将源文件项和拆分结果保存为元组
    else:
        # 对于不包含关键词的项，拆分点前后留空
        split_items.append((item, '', ''))

# 4）将可以分列的项进行分列
split_result = pd.DataFrame(split_items, columns=['源文件项', '拆分点前', '拆分点后'])

# 5）写入分列后的结果，使用相对路径
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file_path = f"../../PY/数据处理/按关键词拆列_{timestamp}.xlsx"
split_result.to_excel(output_file_path, index=False)

print(f"文件已成功写入：{output_file_path}")