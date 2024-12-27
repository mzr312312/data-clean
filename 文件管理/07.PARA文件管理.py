import pandas as pd
import os
import shutil

"""
这个脚本用于管理抖音视频文件。它从一个Excel文件中读取视频文件的分类和原始文件名，
根据分类将视频文件移动到相应的文件夹中。

使用方法：
1. 确保安装了pandas库：可以通过命令 `pip install pandas` 安装。
2. 将Excel文件放置在指定路径中，路径在代码中设定为 'I:\抖音收藏\抖音视频管理.xlsx'。
3. Excel文件中需包含“分类”和“原始文件名”两列，
   - “分类”列用于指定文件应移动到的文件夹名称。
   - “原始文件名”列用于指定需要移动的文件的名称。
4. 运行此脚本，脚本会自动创建缺失的分类文件夹并移动相关文件。

注意事项：
- 确保原始文件名在指定路径下存在，否则将会跳过这些文件的移动，并在控制台中输出提示信息。
- 请根据实际情况修改脚本中的文件路径。

"""


# 读取Excel文件
excel_file = r'I:\抖音收藏\抖音视频管理.xlsx'
df = pd.read_excel(excel_file)

# 获取分类列并去重
categories = df['分类'].drop_duplicates().tolist()

# 在“I:\抖音收藏”文件夹内生成对应的文件夹
base_dir = r'I:\抖音收藏'
for category in categories:
    category_dir = os.path.join(base_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

# 根据“分类”里的类型和对应的“原始文件名”，把文件移动到对应的文件夹中
for index, row in df.iterrows():
    original_filename = row['原始文件名']
    category = row['分类']
    source_file = os.path.join(base_dir, original_filename)
    destination_dir = os.path.join(base_dir, category)

    # 检查源文件是否存在
    if os.path.exists(source_file):
        shutil.move(source_file, destination_dir)
    else:
        print(f"文件 {original_filename} 不存在，跳过移动。")

print("文件移动完成。")