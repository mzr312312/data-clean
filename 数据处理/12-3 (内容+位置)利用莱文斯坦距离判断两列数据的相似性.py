"""
脚本名称: 利用莱文斯坦距离判断两列数据的相似性

描述:
本脚本旨在读取一个Excel文件，并使用莱文斯坦距离（影响因素：字符的相似性和字符位置的相似性）来计算两列数据的相似度评分。相似度评分越高，表示两列数据之间的相似性越强。评分范围为0到100，100表示完全相同，0表示完全不同。

使用方法:
1. 确保已安装pandas库，用于读取Excel文件。
2. 安装Levenshtein库，以便能够计算莱文斯坦距离。
3. 修改`input_file`变量，指定要读取的Excel文件路径（此脚本使用相对路径，请根据实际情况修改）。
4. 确保Excel文件中包含名为'要对比的列1'和'要对比的列2'的列。
5. 运行脚本，结果将会在新的一列中输出相似度评分。

注意事项:
- 如果要对比的列中的数据为空字符串，则相似度评分将返回100。
- 此脚本假设输入数据的格式正确，未对数据有效性进行详细验证。

作者: 马卓然
日期: 2024年11月15日
"""

import pandas as pd
import Levenshtein as lev
import datetime

# 读取Excel文件
input_file = '../PY/数据处理/12-3 利用莱文斯坦距离判断两列数据的相似性.xlsx'
df = pd.read_excel(input_file)

# 检查列名
assert '要对比的列1' in df.columns and '要对比的列2' in df.columns, '确保列名正确'

# 计算莱文斯坦距离并将相似度评分放在新的一列中
def similarity_score(row):
    # 计算莱文斯坦距离
    distance = lev.distance(row['要对比的列1'], row['要对比的列2'])
    max_len = max(len(row['要对比的列1']), len(row['要对比的列2']))

    # 计算相似度分数，分数越高相似度越高
    if max_len == 0:  # 防止除以零
        return 100.0  # 如果两者都是空字符串，则评分为100%
    score = 1 - distance / max_len
    score = round(score * 100, 2)  # 将评分转换为0~100，并保留两位小数
    return score

# 应用到每一行
df['相似度评分'] = df.apply(similarity_score, axis=1)

# 生成带时间戳的输出文件名
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'../../PY/数据处理/两列数据评分_{timestamp}.xlsx'

# 输出到Excel文件
df.to_excel(output_file, index=False)

print(f'相似度评分已保存到：{output_file}')
