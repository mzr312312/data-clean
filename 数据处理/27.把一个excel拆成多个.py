import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# =============== 默认配置参数 ===============
default_sheet_name = '审核数据'  # 要拆分的 sheet 名称
default_header_rows = 1         # 标题行数（1、2 或 3）
default_rows_per_file = 500     # 每个文件包含多少行数据
output_folder = r'../../PY/数据处理/27.拆分出来的excel文件'  # 输出路径保持不变


def select_input_file():
    file_path = filedialog.askopenfilename(
        title="选择要拆分的 Excel 文件",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)


def start_splitting():
    input_file = input_entry.get().strip()

    # 获取用户输入的配置
    sheet_name = sheet_entry.get().strip()
    try:
        header_rows = int(header_entry.get())
        rows_per_file = int(rows_entry.get())
    except ValueError:
        messagebox.showerror("错误", "标题行数和每文件行数必须是整数！")
        return

    if not os.path.isfile(input_file):
        messagebox.showerror("错误", "输入文件路径无效！")
        return

    try:
        df = pd.read_excel(input_file, sheet_name=sheet_name, header=None)
        print(f"读取完成：{input_file} 中的 {sheet_name}")
    except Exception as e:
        messagebox.showerror("错误", f"无法读取 Excel 表单页: {e}")
        return

    headers = df.iloc[:header_rows]
    data_df = df.iloc[header_rows:].reset_index(drop=True)

    total_rows = len(data_df)
    print(f"总数据行数: {total_rows} 行")

    os.makedirs(output_folder, exist_ok=True)

    file_count = 0
    start_row = 0

    while start_row < total_rows:
        file_count += 1
        end_row = min(start_row + rows_per_file, total_rows)

        current_data = pd.concat([headers, data_df.iloc[start_row:end_row]], ignore_index=True)

        file_start = start_row + 1
        file_end = end_row
        output_filename = f"{file_count:03d}_{file_start}-{file_end}行.xlsx"
        output_path = os.path.join(output_folder, output_filename)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            current_data.to_excel(writer, sheet_name=sheet_name, index=False, header=None)

        print(f"已生成：{output_filename}")
        start_row = end_row

    messagebox.showinfo("完成", f"文件已成功拆分到：\n{output_folder}")


# 创建主窗口
root = tk.Tk()
root.title("Excel 拆分工具 - 配置参数")
root.geometry("600x450")

# 输入文件
tk.Label(root, text="请选择输入的 Excel 文件:").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)
tk.Button(root, text="浏览...", command=select_input_file).pack(pady=5)

# Sheet 名称
tk.Label(root, text="Sheet 名称:").pack(pady=5)
sheet_entry = tk.Entry(root, width=30)
sheet_entry.insert(0, default_sheet_name)
sheet_entry.pack(pady=5)

# 标题行数
tk.Label(root, text="标题行数 (1, 2 或 3):").pack(pady=5)
header_entry = tk.Entry(root, width=10)
header_entry.insert(0, str(default_header_rows))
header_entry.pack(pady=5)

# 每个文件行数
tk.Label(root, text="每文件包含行数:").pack(pady=5)
rows_entry = tk.Entry(root, width=10)
rows_entry.insert(0, str(default_rows_per_file))
rows_entry.pack(pady=5)

# 开始按钮
tk.Button(root, text="开始拆分", command=start_splitting, bg="green", fg="white").pack(pady=20)

# 启动GUI
root.mainloop()