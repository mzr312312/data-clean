import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QMenu, \
    QAction, QLabel, QTableWidget, QTableWidgetItem, QTextEdit, QComboBox, QPushButton
from PyQt5.QtCore import QModelIndex, Qt, QEvent
from PyQt5.QtWidgets import QFileSystemModel
import os
import shutil
import pandas as pd
import subprocess


class FileExplorer(QMainWindow):
    def __init__(self, left_directory_path, right_directory_path, script_directory_path):
        super().__init__()

        self.setWindowTitle("Dual File Explorer with Excel Preview and Script Runner")
        self.setGeometry(100, 100, 1400, 800)

        # 创建一个主布局
        main_layout = QHBoxLayout()

        # 左边的文件浏览器
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # 添加下拉单选框和运行按钮
        self.script_combo = QComboBox()
        self.populate_script_combo(script_directory_path)
        left_layout.addWidget(self.script_combo)

        self.run_button = QPushButton("Run in PyCharm")
        self.run_button.clicked.connect(self.run_selected_script)
        left_layout.addWidget(self.run_button)

        left_label = QLabel("输入文件")
        left_layout.addWidget(left_label)
        self.left_tree = self.create_file_browser(left_directory_path)
        left_layout.addWidget(self.left_tree)
        left_widget.setLayout(left_layout)

        # 右边的文件浏览器
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_label = QLabel("输出文件")
        right_layout.addWidget(right_label)
        self.right_tree = self.create_file_browser(right_directory_path)
        right_layout.addWidget(self.right_tree)
        right_widget.setLayout(right_layout)

        # 创建一个垂直分割器来分隔左右两个窗口
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # 预览窗口
        preview_widget = QWidget()
        preview_layout = QVBoxLayout()
        preview_label = QLabel("数据预览")
        preview_layout.addWidget(preview_label)
        self.preview_table = QTableWidget()
        self.preview_text = QTextEdit("No file selected for preview.")

        preview_layout.addWidget(self.preview_table)
        preview_layout.addWidget(self.preview_text)
        preview_widget.setLayout(preview_layout)

        # 创建一个水平分割器来分隔文件浏览器和预览窗口
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(splitter)
        main_splitter.addWidget(preview_widget)
        main_splitter.setSizes([800, 600])  # 设置初始大小

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(main_layout)
        main_layout.addWidget(main_splitter)
        self.setCentralWidget(container)

    def populate_script_combo(self, directory_path):
        # 扫描目录中的 .py 文件
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    self.script_combo.addItem(os.path.join(root, file))

    def run_selected_script(self):
        # 获取选中的脚本路径
        script_path = self.script_combo.currentText()
        if not script_path:
            return

        try:
            # 使用 charm 命令在 PyCharm 中打开并运行脚本
            subprocess.Popen(['charm', 'open', script_path])
            subprocess.Popen(['charm', 'run', script_path])
        except Exception as e:
            print(f"Error running {script_path} in PyCharm: {e}")

    def create_file_browser(self, directory_path):
        # 创建一个 QFileSystemModel 并设置根路径
        model = QFileSystemModel()
        model.setRootPath(directory_path)

        # 创建一个 QTreeView 控件并设置模型
        tree = QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(directory_path))
        tree.setColumnWidth(0, 250)  # 设置第一列（名称）的宽度
        tree.setAlternatingRowColors(True)  # 交替行颜色

        # 连接 doubleClicked 信号到 open_file 方法
        tree.doubleClicked.connect(lambda index: self.open_file(index, model))

        # 安装事件过滤器来捕获键盘事件
        tree.installEventFilter(self)

        # 设置右键菜单
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.customContextMenuRequested.connect(lambda pos: self.show_context_menu(tree, model, pos))

        return tree

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            # 获取当前选中的索引
            indexes = obj.selectedIndexes()
            if indexes:
                self.delete_files(indexes, obj.model())
            return True
        return super().eventFilter(obj, event)

    def show_context_menu(self, tree, model, pos):
        index = tree.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_files([index], model))

        open_action = QAction("Open with Excel", self)
        open_action.triggered.connect(lambda: self.open_with_excel(model.filePath(index)))

        menu.addAction(delete_action)
        menu.addAction(open_action)
        menu.exec_(tree.viewport().mapToGlobal(pos))

    def delete_files(self, indexes, model):
        for index in indexes:
            file_path = model.filePath(index)
            try:
                if model.isDir(index):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                model.remove(index)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    def open_file(self, index, model):
        # 获取文件路径
        file_path = model.filePath(index)

        # 检查是否为文件
        if model.isDir(index):
            return  # 如果是目录则不执行任何操作

        # 使用默认应用程序打开文件
        if file_path.lower().endswith(('.xlsx', '.xls')):
            self.preview_excel(file_path)
        else:
            os.startfile(file_path)

    def open_with_excel(self, file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            print(f"Error opening {file_path} with Excel: {e}")

    def preview_excel(self, file_path):
        try:
            # 读取 Excel 文件
            df = pd.read_excel(file_path)

            # 清空表格
            self.preview_table.clear()
            self.preview_table.setRowCount(df.shape[0])
            self.preview_table.setColumnCount(df.shape[1])
            self.preview_table.setHorizontalHeaderLabels(df.columns)

            # 填充表格
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iat[row, col]))
                    self.preview_table.setItem(row, col, item)

            # 显示预览信息
            self.preview_text.setText(f"Previewing: {file_path}")
        except Exception as e:
            self.preview_text.setText(f"Error previewing {file_path}: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 指定要浏览的目录
    left_directory_to_explore = r"C:\Users\JA085914\Desktop\PY\数据处理"  # 更改为你要显示的左目录路径
    right_directory_to_explore = r"C:\Users\JA085914\Desktop\PY\数据处理\输出文件"  # 更改为你要显示的右目录路径
    script_directory_path = r"D:\PycharmProjects\pythonProject\数据处理"  # 用于读取 .py 脚本的目录

    explorer = FileExplorer(left_directory_to_explore, right_directory_to_explore, script_directory_path)
    explorer.show()

    sys.exit(app.exec_())