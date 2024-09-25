import pandas as pd

# 设置pandas显示所有列
# 所有列不能有空格，否则跑不通
# 用“none”和数字0填充所有空格（见脚本：00.把表格填满.py）
# 设置读取excel文件的路径
# 在底部设置


# 手动填写Excel文件的路径
excel_path = r'D:\Factory\BOM清单V1.2(20240826).xlsx'

# 读取Excel文件
df = pd.read_excel(excel_path)

# 初始化一个空的列表来存储每一行的数据
data = []

# 遍历DataFrame的每一行
for index, row in df.iterrows():
    # 初始化一个空的字典来存储当前行的数据
    row_data = {}

    # 添加工艺名
    row_data['工艺名'] = row['工艺名']

    # 添加输出产品及其数量
    for i in range(1, 4):
        product_name_col = f'输出{i}'
        product_quantity_col = f'输出{i}数量'
        if pd.notna(row[product_name_col]):
            row_data[product_name_col] = row[product_name_col]
            row_data[product_quantity_col] = float(row[product_quantity_col])

    # 添加输入原材料及其数量
    for i in range(1, 7):
        material_name_col = f'输入{i}'
        material_quantity_col = f'输入{i}数量'
        if pd.notna(row[material_name_col]):
            row_data[material_name_col] = row[material_name_col]
            row_data[material_quantity_col] = float(row[material_quantity_col])

    # 添加生产设备
    for i in range(1, 4):
        equipment_col = f'生产设备{i}'
        if pd.notna(row[equipment_col]):
            row_data[equipment_col] = row[equipment_col]

    # 添加分类和制造时间
    row_data['分类'] = row['分类']
    row_data['制造时间'] = float(row['制造时间'])

    # 将当前行的数据添加到列表中
    data.append(row_data)

# 将列表转换为DataFrame
data_df = pd.DataFrame(data)

# 将“工艺名”列设置为索引
data_df.set_index('工艺名', inplace=True)

# 打印DataFrame
print(data_df)
