import pandas as pd
import os
from datetime import datetime

# 定义输入文件路径和输出文件路径（相对路径）
input_file = r"../PY/数据处理/24.合并单元格拆开后向下填充.xlsx"
output_dir = os.path.dirname(input_file)

# 读取 Excel 文件
df = pd.read_excel(input_file)

# 遍历每一列，填充空单元格
for col in df.columns:
    # 使用 forward fill 方法填充空单元格
    df[col] = df[col].ffill()

# 生成带有时间戳的输出文件名
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = os.path.join(output_dir, f"填充{timestamp}.xlsx")

# 将结果保存到新的 Excel 文件
df.to_excel(output_file, index=False)

print(f"填充完成，输出文件已保存为：{output_file}")