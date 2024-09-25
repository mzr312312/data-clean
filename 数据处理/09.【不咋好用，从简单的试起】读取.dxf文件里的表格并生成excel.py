import ezdxf
import pandas as pd
from datetime import datetime
import os


def read_table_from_dxf(dxf_file_path):
    # 加载DXF文件
    doc = ezdxf.readfile(dxf_file_path)

    # 获取模型空间
    msp = doc.modelspace()

    # 定义一个函数来查找表格中的行
    def find_rows():
        rows = []
        current_row = []
        y_position = None
        x_positions = []
        for entity in msp:
            if entity.dxftype() == 'TEXT':
                # 使用insert属性获取位置
                if not current_row or (entity.dxf.insert[1] == y_position):
                    # 检查x坐标是否接近现有列的x坐标
                    closest_x = min(x_positions, key=lambda x: abs(x - entity.dxf.insert[0]), default=None)
                    if closest_x is None or abs(closest_x - entity.dxf.insert[0]) <= 0.01:  # 调整这个阈值以适应您的表格
                        current_row.append(entity)
                        x_positions.append(entity.dxf.insert[0])
                    y_position = entity.dxf.insert[1]
                else:
                    rows.append(current_row)
                    current_row = [entity]
                    x_positions = [entity.dxf.insert[0]]
                    y_position = entity.dxf.insert[1]
        if current_row:
            rows.append(current_row)
        return rows

    # 查找所有行
    all_rows = find_rows()

    # 提取文本数据
    data = []
    for row in all_rows:
        row_data = [entity.dxf.text for entity in row]
        data.append(row_data)

    return data


# 设置文件路径
input_dxf_file_path = r'E:\工作\2.方案设计\2 数采工作\1 各基地\01 石家庄基地\0 石家庄资料\各系统\11 污水处理系统\3 图纸\设备清单.dxf'

# 输出文件路径
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_folder = os.path.dirname(input_dxf_file_path)
output_excel_file_path = os.path.join(output_folder, f'设备清单_{timestamp}.xlsx')

# 读取表格数据
table_data = read_table_from_dxf(input_dxf_file_path)

# 创建DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# 保存为Excel文件
df.to_excel(output_excel_file_path, index=False)

print("转换完成！")