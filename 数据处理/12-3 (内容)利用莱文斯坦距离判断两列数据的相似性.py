import pandas as pd
import Levenshtein as lev
import datetime
from collections import Counter
"""
本脚本用于读取Excel文件中的两列数据，并利用字符出现频率计算这两列数据的相似度评分。输出的评分会被添加到新的列中，并最终保存为一个新的Excel文件。

使用方法：
1. 确保安装了所需的库：pandas、Levenshtein和collections。
2. 将要对比的Excel文件放在指定路径下。输入文件路径为相对路径：'../PY/数据处理/12-3 利用莱文斯坦距离判断两列数据的相似性.xlsx'。
3. 确保Excel文件中包含名为“要对比的列1”和“要对比的列2”的列。
4. 运行脚本，它将自动读取Excel文件，计算相似度评分并保存到新的Excel文件中。
5. 输出文件的名称将包含时间戳，以确保每次运行都有唯一的文件名，输出文件路径也是相对路径，格式为'../../PY/数据处理/两列数据评分_时间戳.xlsx'。

注意事项：
- 请确保Excel文件的结构正确，即包含需要比较的两列数据。
- 此脚本通过计算字符出现频率来判断两列数据的相似度，不考虑字符位置。
- 如果两列数据都是空字符串，将返回相似度100.0。

依赖库：
- pandas：用于数据处理。
- Levenshtein：用于计算莱文斯坦距离（未在此脚本中直接使用）。
- collections：用于计算字符频率的Counter类。

作者: 马卓然
日期: 2024年11月15日
"""

# 读取Excel文件
input_file = '../PY/数据处理/12-3 利用莱文斯坦距离判断两列数据的相似性.xlsx'
df = pd.read_excel(input_file)

# 检查列名
assert '要对比的列1' in df.columns and '要对比的列2' in df.columns, '确保列名正确'

# 计算莱文斯坦距离并将相似度评分放在新的一列中


def similarity_score(row):
    # 计算字符频率
    counter1 = Counter(row['要对比的列1'])
    counter2 = Counter(row['要对比的列2'])

    # 计算内容的相似度
    total_characters = len(set(counter1.keys()).union(set(counter2.keys())))  # 获取所有不同字符的总数
    if total_characters == 0:  # 如果两者都是空字符串
        return 100.0

    # 计算相似的字符总数
    common_characters = sum((counter1 & counter2).values())  # 计算相同字符的总数
    score = (common_characters / total_characters) * 100  # 计算相似度百分比
    return round(score, 2)


# 应用到每一行
df['相似度评分'] = df.apply(similarity_score, axis=1)

# 生成带时间戳的输出文件名
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'../../PY/数据处理/两列数据评分_{timestamp}.xlsx'

# 输出到Excel文件
df.to_excel(output_file, index=False)

print(f'相似度评分已保存到：{output_file}')
