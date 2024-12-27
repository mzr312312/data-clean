import os
from openpyxl import Workbook

"""
该脚本用于遍历指定目录下的所有文件，并将文件名及其分类（文件夹名称）导出到一个Excel文件中。

使用方法：
1. 将 'directory' 变量的值替换为你希望遍历的文件夹路径。
2. 将 'output_file' 变量的值替换为你希望保存的Excel文件的路径和文件名。
3. 运行该脚本，程序将自动扫描指定文件夹中的所有文件，并将它们的名称和分类写入Excel文件。
4. 输出的Excel文件将包含两个列：原始文件名 和 分类。

依赖库：
- os：用于进行文件和目录的操作。
- openpyxl：用于创建和操作Excel文件。

注意：
请确保在运行该脚本之前已经安装了 openpyxl 库，可以使用以下命令进行安装：
pip install openpyxl
"""

def get_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            folder_name = os.path.dirname(relative_path)
            all_files.append((file, folder_name))
    return all_files


def write_to_excel(file_list, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "文件列表"
    ws.append(["原始文件名", "分类"])

    for file_name, folder_name in file_list:
        ws.append([file_name, folder_name])

    wb.save(output_file)


if __name__ == "__main__":
    directory = "I:\抖音收藏"  # 替换为你的文件夹路径
    output_file = "I:\抖音收藏\文件列表.xlsx"  # 替换为你想保存的Excel文件名

    all_files = get_all_files(directory)
    write_to_excel(all_files, output_file)

    print(f"文件名和分类已写入 {output_file}")