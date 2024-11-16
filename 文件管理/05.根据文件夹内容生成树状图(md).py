import os
import tkinter as tk
from tkinter import filedialog

def generate_tree_format(startpath, prefix=''):
    # 要忽略的文件夹名称
    ignore_folders = {'.git', '.idea', '.venv', 'venv'}
    items = os.listdir(startpath)
    total_items = len(items)
    for index, item in enumerate(items):
        if item in ignore_folders:
            continue  # 如果是忽略的文件夹则跳过
        path = os.path.join(startpath, item)
        connector = '└── ' if index == total_items - 1 else '├── '
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = '    ' if connector == '├── ' else '       '
            generate_tree_format(path, prefix + extension)

# 创建一个简单的GUI窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
folder_path = filedialog.askdirectory(title='选择文件夹')  # 打开文件夹选择对话框

if folder_path:  # 如果选择了文件夹
    print(folder_path + '/')
    generate_tree_format(folder_path)
else:
    print("未选择文件夹！")
