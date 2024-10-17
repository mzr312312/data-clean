import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime

# 读取输入Excel文件
input_file_path = r"C:\Users\JA085914\Desktop\PY\数据处理\12-2 利用莱文斯坦距离对一列数据进行归类.py.xlsx"
sheet_name = "Sheet1"  # 根据您的文件内容更改这个名称
data = pd.read_excel(input_file_path, sheet_name=sheet_name)

# 获取“数据放这里”这一列并确保数据都是字符串
data_column = data["数据放这里"].dropna().astype(str).tolist()

# 归类逻辑
categories = {}

for item in data_column:
    found = False
    for key in list(categories.keys()):
        # 计算相似度
        if fuzz.ratio(item, key) > 90:  # 阈值可以调节
            categories[key].add(item)  # 使用集合来避免重复
            found = True
            break
    if not found:
        categories[item] = {item}  # 创建新类别，使用集合

# 构建输出数据框并排序归类项
output_data = []
for key, items in categories.items():
    sorted_items = sorted(items, key=lambda x: fuzz.ratio(x, key), reverse=True)  # 按相似度排序
    output_data.append([key] + sorted_items)  # 将排序后的列表添加到输出数据中

# 创建新的 DataFrame
output_df = pd.DataFrame(output_data)

# 修改列名
output_df.columns = ['类别'] + [f'归类项{i + 1}' for i in range(output_df.shape[1] - 1)]

# 输出文件名及路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = f"C:\\Users\\JA085914\\Desktop\\PY\\数据处理\\Z归类结果_{timestamp}.xlsx"

# 保存到新的Excel文件
output_df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f'归类结果已保存至：{output_file_path}')
