import sys
import json
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_task_selector import TaskSelectorDialog


class Ui_TaskEditor(object):
    def setupUi(self, Form):
        Form.setObjectName("TaskEditor")
        Form.setWindowTitle("蓝牙测试任务编辑器")
        Form.resize(800, 600)

        # 主布局
        self.central_widget = QtWidgets.QWidget(Form)
        Form.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # 左侧按钮区
        self.left_panel = QtWidgets.QVBoxLayout()
        self.left_panel.setSpacing(15)

        # 标题
        self.label = QtWidgets.QLabel("任务列表")
        font = QtGui.QFont("Microsoft YaHei", 18, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.left_panel.addWidget(self.label)

        # 任务列表
        self.task_list = QtWidgets.QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
            }
        """)
        self.task_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # 功能按钮
        self.btn_add = QtWidgets.QPushButton("➕ 添加任务")
        self.btn_edit = QtWidgets.QPushButton("✏️ 编辑任务")
        self.btn_del = QtWidgets.QPushButton("🗑️ 删除任务")
        self.btn_save = QtWidgets.QPushButton("💾 保存配置")
        self.btn_load = QtWidgets.QPushButton("📂 加载配置")

        # 按钮样式
        button_style = """
        QPushButton {
            font-size: 14px;
            min-height: 40px;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: left;
            padding-left: 15px;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        """
        for btn in [self.btn_add, self.btn_edit, self.btn_del, self.btn_save, self.btn_load]:
            btn.setStyleSheet(button_style)
            self.left_panel.addWidget(btn)

        self.left_panel.addStretch()
        self.main_layout.addLayout(self.left_panel, 1)
        self.main_layout.addWidget(self.task_list, 3)


class TaskEditorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TaskEditor()
        self.ui.setupUi(self)

        # 初始化配置目录
        self.config_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../config'))
        os.makedirs(self.config_dir, exist_ok=True)

        # 初始化任务列表
        self.current_file = os.path.join(self.config_dir, 'config.json')
        self.load_config(self.current_file)

        # 连接信号槽
        self.ui.btn_add.clicked.connect(self.add_task)
        self.ui.btn_edit.clicked.connect(self.edit_task)
        self.ui.btn_del.clicked.connect(self.delete_task)
        self.ui.btn_save.clicked.connect(self.save_tasks)
        self.ui.btn_load.clicked.connect(self.load_config_dialog)
        self.ui.task_list.itemDoubleClicked.connect(self.edit_task)

    def add_task(self):
        """添加新任务"""
        selector = TaskSelectorDialog(self)
        if selector.exec_() == QtWidgets.QDialog.Accepted:
            task = selector.get_selected_task()
            self.add_task_item(task['name'], task['repeat'])

    def edit_task(self):
        """编辑选中任务"""
        selected_item = self.ui.task_list.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "警告", "请先选择要编辑的任务")
            return

        # 解析当前任务信息
        item_text = selected_item.text()
        name, repeat = item_text.split(' (x')
        repeat = int(repeat.replace(')', ''))

        # 打开编辑对话框
        selector = TaskSelectorDialog(self)
        selector.combo.setCurrentText(name)
        selector.spin.setValue(repeat)

        if selector.exec_() == QtWidgets.QDialog.Accepted:
            new_task = selector.get_selected_task()
            selected_item.setText(f"{new_task['name']} (x{new_task['repeat']})")

    def delete_task(self):
        """删除选中任务"""
        if self.ui.task_list.currentItem():
            reply = QtWidgets.QMessageBox.question(
                self, "确认删除",
                "确定要删除选中的任务吗？",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.task_list.takeItem(self.ui.task_list.currentRow())

    def save_tasks(self):
        """保存任务到配置文件"""
        if not self.ui.task_list.count():
            QtWidgets.QMessageBox.warning(self, "警告", "任务列表为空")
            return

        try:
            self.save_config(self.current_file)
            QtWidgets.QMessageBox.information(
                self, "保存成功",
                f"配置已保存到:\n{os.path.abspath(self.current_file)}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "保存失败",
                f"保存文件时出错:\n{str(e)}"
            )

    def save_config(self, file_path):
        """保存配置到指定文件"""
        config = {
            "device": {
                "serial": "R5CW505P3RK",
                "input": {"x": 400, "y": 900}
            },
            "log": {"file_path": "../logs/"},
            "tasks": {}
        }

        # 转换任务格式
        task_group = []
        for index in range(self.ui.task_list.count()):
            item_text = self.ui.task_list.item(index).text()
            name, repeat = item_text.split(' (x')
            repeat = repeat.replace(')', '')
            task_group.append({name: int(repeat)})

        config["tasks"]["custom_task"] = task_group

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

    def load_config_dialog(self):
        """弹出加载文件对话框"""
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "加载配置文件", self.config_dir,
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if file_name:
            self.load_config(file_name)

    def load_config(self, file_path):
        """从配置文件加载任务"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

            self.ui.task_list.clear()
            self.current_file = file_path

            # 加载任务
            if "tasks" in config:
                for task_name, actions in config["tasks"].items():
                    for action in actions:
                        action_type, times = list(action.items())[0]
                        self.add_task_item(action_type, times)

            self.setWindowTitle(f"蓝牙测试任务编辑器 - {os.path.basename(file_path)}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "加载失败",
                f"加载配置文件时出错:\n{str(e)}"
            )

    def add_task_item(self, name, repeat):
        """添加任务项到列表"""
        item = QtWidgets.QListWidgetItem(f"{name} (x{repeat})")
        self.ui.task_list.addItem(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))

    # 设置样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
    """)

    window = TaskEditorWindow()
    window.show()
    sys.exit(app.exec_())