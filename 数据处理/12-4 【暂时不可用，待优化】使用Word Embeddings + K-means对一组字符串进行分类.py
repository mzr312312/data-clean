"""
该脚本用于对一组字符串进行聚类，使用预训练的Word2Vec模型（word2vec-google-zh-news-300）通过Word Embeddings和K-means算法生成分组结果。

功能说明：
1. 从指定的 Excel 文件 (file_path) 中读取字符串数据，并将其存储为列表。
2. 使用预训练的Word2Vec模型将字符串转换为词向量。
3. 使用K-means算法对词向量进行聚类，根据指定的聚类数量生成分组结果。
4. 输出结果到新的 Excel 文件中，包含原始字符串及其对应的分组编号。

使用方法：
- 修改 `file_path` 变量，指定包含字符串数据的 Excel 文件路径。
- 根据需要调整 `n_clusters` 变量以选择合适的聚类数量。
- 运行脚本，输出分组结果将保存在与脚本同一目录下，文件名带有时间戳以示唯一性。

输出结果：
- 生成的 Excel 文件包含原始字符串及其对应的分组编号，列名为"分组编号"。

"""

import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
from datetime import datetime
import os

# 第1步：手动下载并加载预训练的Word2Vec模型
model_path = 'word2vec-google-zh-news-300.bin'  # 模型文件名

if not os.path.exists(model_path):
    import urllib.request
    url = 'https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz'
    urllib.request.urlretrieve(url, model_path)

word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

# 第2步：读取Excel文件中的数据
file_path = '../../PY/数据处理/12-2 使用difflib和层次聚类对一组字符串进行分类.xlsx'
df = pd.read_excel(file_path, sheet_name=0)
strings = df.iloc[:, 0].tolist()  # 获取第一列数据并转为列表

# 第3步：将字符串转换为词向量
def get_vector(string):
    words = string.split()  # 将字符串分割为单词
    word_vectors = []
    for word in words:
        if word in word2vec_model:
            word_vectors.append(word2vec_model[word])
    if word_vectors:
        return np.mean(word_vectors, axis=0)  # 计算词向量的平均值
    else:
        return np.zeros(word2vec_model.vector_size)  # 返回零向量

# 将所有字符串转换为词向量
vectors = np.array([get_vector(string) for string in strings])

# 第4步：使用K-means进行聚类
n_clusters = 5  # 可以修改聚类数量
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(vectors)
group_labels = kmeans.labels_

# 第5步：输出分组结果到Excel
output_df = pd.DataFrame({
    '原始数据': strings,
    '分组编号': group_labels
})

# 获取当前时间并格式化为字符串
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f'../../PY/数据处理/分组结果_{current_time}.xlsx'

# 保存到Excel
output_df.to_excel(output_file_path, index=False)

print("分组结果已保存到:", output_file_path)