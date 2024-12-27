import os
import pandas as pd

"""
这个脚本用于根据给定的Excel文件批量重命名指定文件夹中的文件。

使用方法：
1. 确保已安装pandas库，可以通过命令 `pip install pandas` 安装。
2. 将需要重命名的文件的原始文件名和新文件名记录在Excel文件中，并分别放在“原始文件名”和“新文件名”两列中。
3. 修改代码中的`excel_path`变量，将其指向你的Excel文件路径。
4. 修改代码中的`folder_path`变量，将其指向你希望进行文件重命名的目标文件夹路径。
5. 运行此脚本，它将遍历指定文件夹及其子文件夹，查找匹配的原始文件名，并将其重命名为新的文件名。
6. 脚本执行完成后，会输出每个重命名操作的详细信息，并提示“文件名修改完成”。

注意事项：
- 请确保原始文件名在Excel文件中的列名是“原始文件名”，新文件名的列名是“新文件名”，否则代码可能无法正常工作。
- 在执行重命名操作之前，请务必备份重要数据，以免因错误重命名导致文件丢失。
"""


# 读取Excel文件
excel_path = r'I:\抖音收藏\文件列表.xlsx'
df = pd.read_excel(excel_path)

# 获取原始文件名和新文件名的对应关系
original_to_new = dict(zip(df['原始文件名'], df['新文件名']))

# 遍历文件夹及其子文件夹
folder_path = r'I:\抖音收藏'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file in original_to_new:
            original_file_path = os.path.join(root, file)
            new_file_name = original_to_new[file]
            new_file_path = os.path.join(root, new_file_name)

            # 重命名文件
            os.rename(original_file_path, new_file_path)
            print(f'Renamed: {original_file_path} -> {new_file_path}')

print("文件名修改完成。")