import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

# 获取当前脚本的目录
current_dir = os.path.dirname(__file__)
scripts_folder = os.path.join(current_dir, 'scripts')
input_folder = os.path.join(current_dir, '..', 'inputs')
output_folder = os.path.join(current_dir, '..', 'outputs')

# 创建主窗口
root = tk.Tk()
root.title("数据清洗工具")
root.geometry("500x400")


# 脚本文件选择
def choose_script():
    script_path = filedialog.askopenfilename(initialdir=scripts_folder, title="选择脚本文件",
                                             filetypes=(("Python Files", "*.py"),))
    script_entry.delete(0, tk.END)
    script_entry.insert(0, script_path)


# 输入文件选择
def choose_input():
    input_path = filedialog.askopenfilename(initialdir=input_folder, title="选择输入文件",
                                            filetypes=(("Excel Files", "*.xlsx"),))
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)


# 运行脚本
def run_script():
    script_path = script_entry.get()
    input_file = input_entry.get()

    if not script_path or not input_file:
        messagebox.showwarning("警告", "请先选择脚本文件和输入文件")
        return

    # 执行脚本并传入输入文件路径作为参数
    try:
        subprocess.run(['python', script_path, input_file], check=True)
        messagebox.showinfo("成功", "脚本运行成功")
        list_output_files()  # 运行成功后更新输出文件列表
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"脚本运行失败：{str(e)}")


# 列出输出文件
def list_output_files():
    output_listbox.delete(0, tk.END)
    for file_name in os.listdir(output_folder):
        if file_name.endswith('.xlsx'):
            output_listbox.insert(tk.END, file_name)


# 打开选中的输出文件
def open_output_file():
    selected_file = output_listbox.get(tk.ACTIVE)
    if selected_file:
        output_file_path = os.path.join(output_folder, selected_file)
        os.startfile(output_file_path)  # Windows 打开文件的方法


# 创建并放置 GUI 元素
script_label = tk.Label(root, text="选择数据清洗脚本")
script_label.pack(pady=10)

script_entry = tk.Entry(root, width=50)
script_entry.pack(pady=5)

script_button = tk.Button(root, text="选择脚本", command=choose_script)
script_button.pack(pady=5)

input_label = tk.Label(root, text="选择输入文件")
input_label.pack(pady=10)

input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)

input_button = tk.Button(root, text="选择输入文件", command=choose_input)
input_button.pack(pady=5)

run_button = tk.Button(root, text="运行脚本", command=run_script)
run_button.pack(pady=20)

output_label = tk.Label(root, text="输出文件列表")
output_label.pack(pady=10)

output_listbox = tk.Listbox(root, width=50, height=10)
output_listbox.pack(pady=5)

output_button = tk.Button(root, text="打开输出文件", command=open_output_file)
output_button.pack(pady=5)

# 初始化时列出输出文件
list_output_files()

# 启动主循环
root.mainloop()

