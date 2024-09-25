import pandas as pd
from graphviz import Digraph
import os
import datetime

# 以下为代码用途说明：
    # 本代码的功能是，绘制数采电表的层级结构图
    # 输入：Excel文件，包含电表的层级结构清单
    # 该Excel文件应包含6列，这6列分别对应：
    #   1.总进线电表（1级表）；
    #   2.高压侧配电柜馈线电表（2级表）；
    #   3.变压器电表（2级表）（类似11TR3)；
    #   4.配电柜总表（3级表）（类似11301）；
    #   5.回路号（5级表）（类似113LW3）；
    #   6.第5列电表（回路号）的说明，例如，“备用”，“12APH20（空调箱）"等；
    # ***当前没有考虑4级表-抽屉柜电表（母线柜）和6级表（母线插接箱细分电表）的情况，后续添加这部分内容的概率不大（因为有机台电表）
    # ***如果后续有需求，再修改代码添加为8列即可

# 以下为代码使用说明
    # 导入模块后，请将文件路径和sheet名称修改为自己电表的实际路径和名称
    # 运行代码后，会在导入文件所在文件夹生成一个SVG格式的电表结构图文件
    # ***为了便于传播，也可以直接输出pdf格式的文件
    # 每一层级都有自己的颜色，可以根据实际情况调整代码中的颜色设置
    # 打开文件后，可以用浏览器打开查看，也可以用其他软件打开




# 可修改的配置
file_path = r'C:\Users\JA085914\Depython3 -m pip install --upgrade radicale单.xlsx'  # Excel 文件路径
sheet_name = '电池车间'  # 需要读取的 sheet 名称

# 定义颜色
colors = {
    '高压进线': '#FF9999',  # 浅红色
    '高压柜(1)': '#99FF99',  # 浅绿色
    '变压器（2）': '#9999FF',  # 浅蓝色
    '电表号（3）': '#FFFF99',  # 浅黄色
    '回路号（4）': '#FF99FF',  # 浅紫色
    '备注': '#99FFFF'  # 淡青色
}

# 输出文件设置
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_name = f"电表结构图_{timestamp}"  # 文件名
output_folder_path = file_path.rsplit('\\', 1)[0]  # 输出路径为与Excel相同文件夹

# 从Excel读取数据
df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="A:F")

# 获取列名称列表
index_columns = ['高压进线', '高压柜(1)', '变压器（2）', '电表号（3）', '回路号（4）']
df.set_index(index_columns, inplace=True)

dot = Digraph(comment='树状结构图', format='svg', encoding='utf-8')
dot.attr(rankdir='LR')  # 设置图的方向为从左到右

visited_nodes = set()

def add_nodes_edges(df, parent_node):
    for index_tuple in df.index:
        current_node = parent_node
        for level, col_name in enumerate(index_columns):
            part_index = index_tuple[:level + 1]
            node_name = '_'.join(map(str, part_index))  # 确保所有元素都是字符串
            if node_name not in visited_nodes:
                color = colors.get(col_name, '#FFFFFF')  # 根据列名获取颜色
                dot.node(node_name, str(index_tuple[level]), fontname="SimSun", shape='box', style='filled', fillcolor=color)
                dot.edge(current_node, node_name)
                visited_nodes.add(node_name)
            current_node = node_name

        # 处理 "备注" 列
        value_node = f"value_{'_'.join(map(str, index_tuple))}"  # 确保值也是字符串
        dot.node(value_node, str(df.loc[index_tuple, '备注']), fontname="SimSun", shape='box', style='filled', fillcolor=colors['备注'])
        dot.edge(current_node, value_node)

dot.node('根节点', '树状结构', fontname="SimSun", shape='box')  # 设置根节点的形状为矩形
add_nodes_edges(df, '根节点')

# 渲染并保存图形
output_path = os.path.join(output_folder_path, output_file_name)
dot.render(output_path, view=True)
os.remove(output_path)  # 删除无后缀的文件