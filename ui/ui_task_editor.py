# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_task_selector import TaskSelectorDialog


class Ui_TaskEditor(object):
    def setupUi(self, Form):
        Form.setObjectName("TaskEditor")
        Form.setWindowTitle("蓝牙测试任务编辑器")
        Form.resize(700, 550)

        # 主布局
        self.central_widget = QtWidgets.QWidget(Form)
        Form.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # 左侧按钮区
        self.left_panel = QtWidgets.QVBoxLayout()

        # 标题
        self.label = QtWidgets.QLabel("任务列表")
        font = QtGui.QFont("Microsoft YaHei", 18, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.left_panel.addWidget(self.label)

        # 任务列表
        self.task_list = QtWidgets.QListWidget()
        self.task_list.setStyleSheet("font-size: 14px;")

        # 功能按钮
        self.btn_add = QtWidgets.QPushButton("添加任务")
        self.btn_del = QtWidgets.QPushButton("删除任务")
        self.btn_save = QtWidgets.QPushButton("保存配置")

        # 统一设置按钮样式
        button_style = """
        QPushButton {
            font-size: 14px;
            min-height: 40px;
            padding: 5px;
        }
        """
        for btn in [self.btn_add, self.btn_del, self.btn_save]:
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

        # 初始化示例任务
        self.ui.task_list.addItems([
            "蓝牙设备扫描 (x3)",
            "信号强度测试 (x5)"
        ])

        # 连接信号槽
        self.ui.btn_add.clicked.connect(self.add_task)
        self.ui.btn_del.clicked.connect(self.delete_task)
        self.ui.btn_save.clicked.connect(self.save_tasks)

    def add_task(self):
        """打开任务选择器添加新任务"""
        selector = TaskSelectorDialog(self)
        if selector.exec_() == QtWidgets.QDialog.Accepted:
            task = selector.get_selected_task()
            self.ui.task_list.addItem(f"{task['name']} (x{task['repeat']})")

    def delete_task(self):
        """删除选中任务"""
        if self.ui.task_list.currentItem():
            self.ui.task_list.takeItem(self.ui.task_list.currentRow())

    def save_tasks(self):
        """保存任务列表"""
        count = self.ui.task_list.count()
        if count > 0:
            QtWidgets.QMessageBox.information(
                self, "保存成功", f"已保存 {count} 个任务")
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "任务列表为空")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))
    window = TaskEditorWindow()
    window.show()
    sys.exit(app.exec_())