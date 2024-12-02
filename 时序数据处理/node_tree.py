import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

diff_values = {}
#

class TreeViewApp(QMainWindow):
    def __init__(self, nodes):
        super().__init__()

        self.setWindowTitle("树状结构显示")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabel("节点")

        self.toggle_button = QPushButton("切换显示格式", self)
        self.toggle_button.clicked.connect(self.toggle_display_format)

        # 默认显示为 node_name : diff值 的格式
        self.display_diff_format = True

        # 找到所有的根节点
        root_nodes = [node for node in nodes if pd.isna(node['parent_node_id'])]

        # 构建树并填充到widget
        for root in root_nodes:
            tree = self.build_tree(nodes, root['node_id'])
            self.populate_tree_widget(tree, self.tree_widget)

        self.layout.addWidget(self.tree_widget)
        self.layout.addWidget(self.toggle_button)

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

        # 根据当前显示格式决定如何显示
        if self.display_diff_format:
            display_text = f"{tree['node_name']} : {tree['diff'] if tree['diff'] is not None else '无'}"
        else:
            display_text = f"{tree['node_name']} (ID: {tree['node_id']}) : {tree['diff'] if tree['diff'] is not None else '无'}KWH"

        item = QTreeWidgetItem(parent_widget, [display_text])
        for child in tree['children']:
            self.populate_tree_widget(child, item)

    def toggle_display_format(self):
        self.display_diff_format = not self.display_diff_format
        self.tree_widget.clear()  # 清空树
        # 重新填充树
        root_nodes = [node for node in load_data('../../PY/时序数据处理/电表层级清单.xlsx') if pd.isna(node['parent_node_id'])]
        for root in root_nodes:
            tree = self.build_tree(load_data('../../PY/时序数据处理/电表层级清单.xlsx'), root['node_id'])
            self.populate_tree_widget(tree, self.tree_widget)

def load_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df.to_dict(orient='records')

if __name__ == '__main__':
    # 读取Excel文件
    file_path = '../../PY/时序数据处理/电表层级清单.xlsx'
    nodes = load_data(file_path)

    app = QApplication(sys.argv)
    window = TreeViewApp(nodes)
    window.show()
    sys.exit(app.exec_())
