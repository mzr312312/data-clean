import os
import openpyxl

# 指定Excel文件的位置
excel_file = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\文件管理_SJ.xlsx'
# 打开Excel工作簿
workbook = openpyxl.load_workbook(excel_file)
# 选择工作表
sheet = workbook['文件夹']

# 指定要创建文件夹的目标目录
target_directory = r'C:\Users\JA085914\Desktop\PY\文件管理\新文件夹'

# 遍历工作表中的每一行，从第二行开始（跳过标题）
for row in sheet.iter_rows(min_row=2, values_only=True):
    folder_name = row[0]  # 假设文件夹名称在每行的第一个单元格
    if folder_name:  # 检查单元格是否有值
        folder_path = os.path.join(target_directory, folder_name)
        if not os.path.exists(folder_path):  # 如果文件夹不存在则创建
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")