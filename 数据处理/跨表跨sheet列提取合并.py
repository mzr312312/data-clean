import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import pandas as pd
from pandas import ExcelWriter
import os
import numpy as np


# 修复函数：安全获取小写列名
def safe_lower(col):
    """安全处理非字符串列名，确保能转换为小写"""
    if isinstance(col, str):
        return col.lower().strip()
    elif isinstance(col, (int, float, np.floating)):
        # 数值类型转为字符串处理
        return str(int(col)) if col.is_integer() else str(col)
    else:
        try:
            # 其他类型尝试强制转换
            return str(col).lower().strip()
        except:
            # 转换失败时返回空字符串
            return ""


def select_files():
    """打开文件对话框选择多个Excel文件"""
    filepaths = filedialog.askopenfilenames(
        title="选择Excel文件",
        filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
    )
    if filepaths:
        files_listbox.delete(0, tk.END)  # 清除旧列表
        for filepath in filepaths:
            files_listbox.insert(tk.END, filepath)


def merge_excel_data():
    """合并Excel数据的核心函数(增强大小写适应性)"""
    # 获取用户输入
    files = files_listbox.get(0, tk.END)
    # 保留用户输入的原始大小写用于最终输出
    original_column_names = [name.strip() for name in columns_entry.get().split(",") if name.strip()]
    # 创建小写列名用于匹配
    column_names_lower = [name.lower() for name in original_column_names]
    header_row = int(header_row_combo.get()) - 1  # 转换为0开始索引

    # 验证输入
    if not files:
        debug_print("错误：请至少选择一个Excel文件！")
        return
    if not original_column_names:
        debug_print("错误：请输入至少一个列名！")
        return
    if header_row < 0:
        debug_print("错误：请选择有效的列名行号(1-5)!")
        return

    debug_print("开始处理...")
    debug_print(f"目标列名: {', '.join(original_column_names)}")
    debug_print(f"列名所在行: {header_row + 1}")  # 显示给用户的是1开始的

    # 初始化结果DataFrame
    result_df = pd.DataFrame(columns=original_column_names)

    # 处理所有文件
    for filepath in files:
        try:
            debug_print(f"\n处理文件: {os.path.basename(filepath)}")
            # 读取所有Sheet页
            xls = pd.ExcelFile(filepath)

            for sheet_name in xls.sheet_names:
                try:
                    # 读取指定Sheet
                    df = pd.read_excel(
                        xls,
                        sheet_name=sheet_name,
                        header=None  # 先不设置列名
                    )

                    # 验证行数是否足够
                    if len(df) <= header_row:
                        debug_print(f"  Sheet '{sheet_name}': 行数不足，跳过")
                        continue

                    # 设置列名 - 使用安全转换处理非字符串列名
                    # 创建临时列名列表
                    temp_columns = []
                    for col in df.iloc[header_row]:
                        temp_columns.append(safe_lower(col) if safe_lower(col) else "unnamed")

                    df.columns = temp_columns

                    # 提取指定列 - 大小写不敏感匹配
                    selected_columns = pd.DataFrame()

                    # 使用safe_lower创建的列名进行匹配
                    for orig_col, lower_col in zip(original_column_names, column_names_lower):
                        if lower_col in df.columns:
                            selected_columns[orig_col] = df.loc[header_row + 1:, lower_col].reset_index(drop=True)
                        else:
                            selected_columns[orig_col] = None
                            debug_print(f"  Sheet '{sheet_name}': 未找到列 '{orig_col}'")

                    # 合并到结果
                    result_df = pd.concat([result_df, selected_columns], ignore_index=True)
                    debug_print(f"  Sheet '{sheet_name}': 提取 {len(selected_columns)} 行")
                except Exception as e:
                    debug_print(f"  Sheet '{sheet_name}' 处理错误: {str(e)}")
        except Exception as e:
            debug_print(f"文件 {os.path.basename(filepath)} 打开错误: {str(e)}")

    # 保存结果
    if not result_df.empty:
        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        if output_path:
            with ExcelWriter(output_path) as writer:
                result_df.to_excel(writer, index=False, sheet_name="汇总数据")
            debug_print(f"\n处理完成! 共合并 {len(result_df)} 行数据")
            debug_print(f"结果保存至: {output_path}")
        else:
            debug_print("操作取消: 未选择保存位置")
    else:
        debug_print("警告: 没有提取到任何数据")


def debug_print(message):
    """在调试窗口打印信息"""
    debug_text.config(state=tk.NORMAL)
    debug_text.insert(tk.END, message + "\n")
    debug_text.see(tk.END)  # 自动滚动到底部
    debug_text.config(state=tk.DISABLED)


# 创建主窗口
root = tk.Tk()
root.title("Excel列合并工具")
root.geometry("800x600")

# 文件选择区域
file_frame = ttk.LabelFrame(root, text="选择Excel文件")
file_frame.pack(fill="x", padx=10, pady=5)

select_button = ttk.Button(file_frame, text="选择文件", command=select_files)
select_button.pack(side="left", padx=5, pady=5)

files_listbox = tk.Listbox(file_frame, height=5, selectmode=tk.EXTENDED)
files_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

scrollbar = ttk.Scrollbar(file_frame, orient="vertical")
scrollbar.config(command=files_listbox.yview)
scrollbar.pack(side="right", fill="y")
files_listbox.config(yscrollcommand=scrollbar.set)

# 设置选项区域
settings_frame = ttk.LabelFrame(root, text="合并设置")
settings_frame.pack(fill="x", padx=10, pady=5)

# 列名设置
columns_frame = ttk.Frame(settings_frame)
columns_frame.pack(fill="x", padx=5, pady=5)
ttk.Label(columns_frame, text="目标列名(英文逗号分隔):").pack(side="left")
columns_entry = ttk.Entry(columns_frame, width=40)
columns_entry.pack(side="left", padx=5, fill="x", expand=True)

# 行号设置
header_row_frame = ttk.Frame(settings_frame)
header_row_frame.pack(fill="x", padx=5, pady=5)
ttk.Label(header_row_frame, text="列名所在行号:").pack(side="left")
header_row_combo = ttk.Combobox(header_row_frame, values=[1, 2, 3, 4, 5], width=5)
header_row_combo.set(1)  # 默认第一行
header_row_combo.pack(side="left", padx=5)

# 操作按钮
action_frame = ttk.Frame(root)
action_frame.pack(pady=10)
merge_button = ttk.Button(action_frame, text="开始合并", command=merge_excel_data)
merge_button.pack()

# 调试信息区域
debug_frame = ttk.LabelFrame(root, text="调试信息")
debug_frame.pack(fill="both", expand=True, padx=10, pady=5)

debug_text = scrolledtext.ScrolledText(
    debug_frame,
    height=10,
    wrap=tk.WORD,
    state=tk.DISABLED
)
debug_text.pack(fill="both", expand=True, padx=5, pady=5)

# 运行主循环
root.mainloop()