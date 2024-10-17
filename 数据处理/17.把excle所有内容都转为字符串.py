import pandas as pd
import os
from datetime import datetime

# 读取Excel文件
file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\1 石家庄资料\01 配电系统\1点表\【王云峰最新】导入临时科林10月8号反馈-项目数据表_数据源及采集点-整体1009.xlsx'  # 替换为你的Excel文件路径

# 获取当前时间戳
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file_name = f"生成str_{timestamp}.xlsx"
output_file_path = os.path.join(os.path.dirname(file_path), output_file_name)

# 读取所有sheet页
xls = pd.ExcelFile(file_path)
df_list = []

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # 将DataFrame中的所有元素转换为字符串，保留空格
    df = df.astype(str).replace({'^\\s*$': ''}, regex=True)  # 将空白单元格替换为''，不为NaN
    df_list.append(df)

# 合并所有sheet的数据
final_df = pd.concat(df_list, ignore_index=True)

# 输出检查
print(final_df)

# 保存修改后的DataFrame到新的Excel文件
final_df.to_excel(output_file_path, index=False)
