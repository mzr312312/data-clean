import pandas as pd
import re
import os
from datetime import datetime
# 适合某一列的结构符合：[英文/数字/英文符号+链接符/或没有链接符+中文]的命名形式，此脚本可以从第一个汉字开始，拆成下一列
# 如果有一些链接符成为小尾巴，使用“08.设备名处理-删除某列尾部的符号.py”处理即可得到干净的设备名
# 需要指定：文件路径、sheet_name，列名
# 自动在文件路径相同文件夹下，生成带时间戳的新文件“split_时间戳”

# 文件路径
file_path = r'D:\PycharmProjects\PY\数据处理\06.设备名处理：从第一个中文字开始拆成另一列.xlsx'

# 读取Excel文件中的特定工作表
df = pd.read_excel(file_path, sheet_name='设备名处理')

# 指定需要处理的列
column_name = '需要处理的列'

# 检查列名是否存在于DataFrame中
if column_name not in df.columns:
    print(f"警告: 列名 '{column_name}' 未在文件中找到。")
else:
    # 定义一个函数，用于拆分字符串
    def split_column(cell_value):
        # 查找第一个中文字符的位置
        match = re.search(r'[\u4e00-\u9fff]', cell_value)
        if match:
            index = match.start()
            # 分割字符串
            before = cell_value[:index]
            after = cell_value[index:]
            return before, after
        else:
            return cell_value, ''

    # 应用函数到DataFrame的一列
    df[[column_name, 'new_column']] = df[column_name].apply(split_column).tolist()

    # 创建输出文件名，包括时间戳
    output_filename = f'split_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
    output_path = os.path.join(os.path.dirname(file_path), output_filename)

    # 将处理后的DataFrame写回Excel文件
    df.to_excel(output_path, index=False)

    print(f"文件已保存到 {output_path}")