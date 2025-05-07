# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_mainWindow import Ui_MainWindow
from ui_task_editor import TaskEditorWindow


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接按钮信号
        self.ui.buttons[0].clicked.connect(self.get_connection)     # 获取连接
        self.ui.buttons[1].clicked.connect(self.open_task_editor)  # 任务编辑按钮
        self.ui.buttons[5].clicked.connect(self.close)  # 退出按钮

        # 初始化设备信息
        self._init_device_info()

    def _init_device_info(self):
        """初始化设备信息显示"""
        info = """设备控制面板 v1.0
-------------------
状态: 未连接
IP: 未配置
任务: 无"""
        self.ui.plainTextEdit.setPlainText(info)

    def open_task_editor(self):
        """打开任务编辑器窗口"""
        self.task_editor = TaskEditorWindow(self)
        self.task_editor.show()

    def get_connection(self):
        """初始化设备信息显示"""
        info = """设备控制面板 v1.0
-------------------
状态: 获取连接（调试ing）
IP: 127.0.0.1
任务: 调试中"""
        self.ui.plainTextEdit.setPlainText(info)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())