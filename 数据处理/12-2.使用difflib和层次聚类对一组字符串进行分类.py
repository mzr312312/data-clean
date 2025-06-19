"""
该脚本用于对一组字符串进行层次聚类，并根据指定的阈值生成分组结果。

功能说明：
1. 从指定的 Excel 文件 (file_path) 中读取字符串数据，并将其存储为列表。
2. 计算字符串之间的相似度矩阵，使用 `difflib` 库中的 `SequenceMatcher` 来评估字符串相似性。
3. 将相似度矩阵转换为距离矩阵，以便进行层次聚类。
4. 使用 SciPy 库中的层次聚类函数 `linkage` 和 `fcluster`，根据给定的阈值对字符串进行分组。
5. 根据设定的阈值（可自由修改,阈值越大，分类数越少，每一类中的字符串越多，最大值为1）动态创建分组编号，并输出结果到新的 Excel 文件中。

使用方法：
- 修改 `file_path` 变量，指定包含字符串数据的 Excel 文件路径。
- 根据需要调整 `thresholds` 列表中的阈值，以便选择合适的分组标准。
- 运行脚本，输出分组结果将保存在与脚本同一目录下，文件名带有时间戳以示唯一性。

输出结果：
- 生成的 Excel 文件包含原始字符串及其对应的分组编号，分组编号列名会根据设置的阈值动态命名。
"""

import pandas as pd
import numpy as np
import difflib
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from datetime import datetime



# 第1步：读取Excel文件中的数据
file_path = '../PY/数据处理/12-2 使用difflib和层次聚类对一组字符串进行分类.xlsx'
df = pd.read_excel(file_path, sheet_name=0)
strings = df.iloc[:, 0].tolist()  # 获取第一列数据并转为列表

# 第2步：计算相似度矩阵
similarity_matrix = np.zeros((len(strings), len(strings)))

for i in range(len(strings)):
    for j in range(len(strings)):
        similarity_matrix[i, j] = difflib.SequenceMatcher(None, strings[i], strings[j]).ratio()

# 第3步：将相似度矩阵转换为距离矩阵
distance_matrix = 1 - similarity_matrix

# 将距离矩阵转换为压缩格式
compressed_distance_matrix = squareform(distance_matrix)

# 第4步：进行层次聚类
Z = linkage(compressed_distance_matrix, method='ward')

# 自由定义阈值
thresholds = [0.6, 0.8, 0.9]  # 可以修改这三个阈值
group_results = {str(threshold): fcluster(Z, threshold, criterion='distance') for threshold in thresholds}

# 第5步：输出分组结果到Excel，使用动态列名
output_data = {'原始数据': strings}
for threshold in thresholds:
    output_data[f'分组编号_阈值={threshold}'] = group_results[str(threshold)]

output_df = pd.DataFrame(output_data)

# 获取当前时间并格式化为字符串
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f'../../PY/数据处理/分组结果_{current_time}.xlsx'

# 保存到Excel
output_df.to_excel(output_file_path, index=False)

print("分组结果已保存到:", output_file_path)
