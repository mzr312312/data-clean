import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
import pandas as pd

# 辅助函数
def calculate_diff_values(file_path):
    df = pd.read_pickle(file_path)
    diff_sum = df.groupby('tagCode')['diff'].sum().round(2)  # 保留两位小数
    return diff_sum.to_dict()

def calculate_time_range(file_path):
    df = pd.read_pickle(file_path)
    start_time = df['time'].min()
    end_time = df['time'].max()
    return {'start_time': start_time, 'end_time': end_time}

def load_data(file_path, diff_values):
    df = pd.read_excel(file_path, engine='openpyxl')
    nodes = df.to_dict(orient='records')
    for node in nodes:
        node['current_diff'] = diff_values.get(node['node_name'], None)
    return nodes

diff_values = calculate_diff_values('combined_cut_df.pkl')

class TreeViewApp(QMainWindow):
    def __init__(self, nodes):
        super().__init__()

        self.setWindowTitle("树状结构显示")
        self.setGeometry(500, 100, 800, 900)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # 初始化按钮
        self.expand_all_button = QPushButton("全部展开", self)
        self.collapse_all_button = QPushButton("全部收起", self)
        self.toggle_button = QPushButton("切换显示格式", self)
        self.export_button = QPushButton("导出到Excel", self)

        # 连接按钮点击事件
        self.expand_all_button.clicked.connect(self.expand_all)
        self.collapse_all_button.clicked.connect(self.collapse_all)
        self.toggle_button.clicked.connect(self.toggle_display_format)
        self.export_button.clicked.connect(self.export_to_excel)

        # 添加时间显示标签
        self.start_time_label = QLabel(self)
        self.end_time_label = QLabel(self)
        self.update_time_labels()

        # 创建TreeWidget
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabel("节点")
        self.tree_widget.setSelectionMode(QTreeWidget.MultiSelection)

        # 创建一个标签来显示选中节点的总 diff 值
        self.total_diff_label = QLabel("选中节点的总 diff 值: 0")

        # 默认显示为 node_name : diff值 的格式
        self.display_diff_format = True

        # 构建并填充树状结构
        root_nodes = [node for node in nodes if pd.isna(node['parent_node_id'])]
        for root in root_nodes:
            tree = self.build_tree(nodes, root['node_id'])
            self.populate_tree_widget(tree, self.tree_widget)

        self.tree_widget.itemSelectionChanged.connect(self.update_diff_total)

        # 将控件添加到布局中
        self.layout.addWidget(self.start_time_label)
        self.layout.addWidget(self.end_time_label)
        self.layout.addWidget(self.total_diff_label)
        self.layout.addWidget(self.tree_widget)

        # 创建一个水平布局用于按钮
        h_layout_buttons = QHBoxLayout()
        h_layout_buttons.addWidget(self.expand_all_button)
        h_layout_buttons.addWidget(self.collapse_all_button)
        h_layout_buttons.addWidget(self.toggle_button)
        h_layout_buttons.addWidget(self.export_button)
        self.layout.addLayout(h_layout_buttons)

    def expand_all(self):
        self.tree_widget.expandAll()  # 展开所有节点

    def collapse_all(self):
        self.tree_widget.collapseAll()  # 收起所有节点

    def update_time_labels(self):
        time_range = calculate_time_range('combined_cut_df.pkl')
        start_time_str = time_range.get('start_time', '未知').strftime('%Y-%m-%d %H:%M:%S') if isinstance(
            time_range.get('start_time'), pd.Timestamp) else '未知'
        end_time_str = time_range.get('end_time', '未知').strftime('%Y-%m-%d %H:%M:%S') if isinstance(
            time_range.get('end_time'), pd.Timestamp) else '未知'
        self.start_time_label.setText(f"起始时间: {start_time_str}")
        self.end_time_label.setText(f"结束时间: {end_time_str}")

    def build_tree(self, nodes, node_id=None):
        current_node = next((node for node in nodes if node['node_id'] == node_id), None)
        if not current_node:
            return None

        children = [self.build_tree(nodes, child['node_id']) for child in nodes if
                    child['parent_node_id'] == current_node['node_id']]

        current_diff = diff_values.get(current_node['node_id'], None)

        return {
            'node_id': current_node['node_id'],
            'node_name': current_node['node_name'],
            'children': children,
            'diff': current_diff
        }

    def populate_tree_widget(self, tree, parent_widget):
        if tree is None:
            return

        if self.display_diff_format:
            display_text = f"{tree['node_name']} : {tree['diff'] if tree['diff'] is not None else '无'}"
        else:
            display_text = f"{tree['node_name']} (ID: {tree['node_id']}) : {tree['diff']:.2f}KWH" if tree[
                                                                                                         'diff'] is not None else f"{tree['node_name']} (ID: {tree['node_id']}) : 无"

        item = QTreeWidgetItem(parent_widget, [display_text])
        for child in tree['children']:
            self.populate_tree_widget(child, item)

    def update_diff_total(self):
        total_diff = 0
        for item in self.tree_widget.selectedItems():
            text = item.text(0)
            parts = text.split(':')
            if len(parts) > 1:
                diff_text = parts[1].strip()
                if diff_text != '无':
                    total_diff += float(diff_text.split()[0])
        self.total_diff_label.setText(f"选中节点的总 diff 值: {total_diff:.2f}")

    def toggle_display_format(self):
        self.display_diff_format = not self.display_diff_format
        self.tree_widget.clear()
        root_nodes = [node for node in load_data('../../PY/时序数据处理/电表层级清单.xlsx') if
                      pd.isna(node['parent_node_id'])]
        for root in root_nodes:
            tree = self.build_tree(load_data('../../PY/时序数据处理/电表层级清单.xlsx'), root['node_id'])
            self.populate_tree_widget(tree, self.tree_widget)

    def export_to_excel(self):
        file_path_to_save = r'../../PY/时序数据处理/导出数据.xlsx'
        data = []

        try:
            self.traverse_tree(self.tree_widget, data)
            df = pd.DataFrame(data, columns=[f'层级{i}' for i in range(max(len(row) for row in data))])
            df.to_excel(file_path_to_save, index=False)
        except Exception as e:
            print(f"发生错误: {e}")

    def traverse_tree(self, widget, data, level=0):
        for index in range(widget.topLevelItemCount()):
            item = widget.topLevelItem(index)
            self.traverse_item(item, data, level)

    def traverse_item(self, item, data, level):
        row = [''] * (level + 1)
        row[level] = item.text(0)
        data.append(row)
        for index in range(item.childCount()):
            child_item = item.child(index)
            self.traverse_item(child_item, data, level + 1)


if __name__ == '__main__':
    file_path = '../../PY/时序数据处理/电表层级清单.xlsx'
    nodes = load_data(file_path, diff_values)

    app = QApplication(sys.argv)
    window = TreeViewApp(nodes)
    window.show()
    sys.exit(app.exec_())