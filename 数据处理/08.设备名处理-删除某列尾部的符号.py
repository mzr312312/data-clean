import pandas as pd
import os
from datetime import datetime
# 目的是，删除某一列内容里，最后一位有一些.或者-之类的小尾巴
# 这一列中各单元格的长度不一样，没有关系
# 设定文件路径，sheet_name，列名
# 自动在文件路径相同文件夹下，生成带时间戳的新文件“删除小尾巴_时间戳”
# 文件路径
file_path = r'..\PY\数据处理\08.设备名处理-删除某列尾部的符号.xlsx'

# 读取Excel文件中的"实验"sheet
df = pd.read_excel(file_path, sheet_name='实验')

# 确保"实验分列"中的所有元素都是字符串
df['实验分列'] = df['实验分列'].astype(str)

# 处理"实验分列"
# 这里是需要删除"实验分列"中的所有尾部的"." 或 "-"符号，如果有其他的，改下就行
def process_cell(cell):
    # 如果最后一个字符是"." 或 "-"，则删除它
    if cell.endswith('.') or cell.endswith('-'):
        return cell[:-1]
    # 其他情况保持不变
    return cell

# 应用处理函数
df['实验分列'] = df['实验分列'].apply(process_cell)

# 获取当前时间作为时间戳
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

# 构建新文件名
new_file_name = f"删除小尾巴_{timestamp}.xlsx"

# 确定保存路径（与源文件同目录）
save_path = os.path.join(os.path.dirname(file_path), new_file_name)

# 保存处理后的数据到新的Excel文件
df.to_excel(save_path, index=False)