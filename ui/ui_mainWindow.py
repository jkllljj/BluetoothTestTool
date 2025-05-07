# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1024, 720)
        MainWindow.setWindowTitle("设备任务控制面板")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # 左侧布局
        self.left_layout = QtWidgets.QVBoxLayout()
        title_font = QtGui.QFont("Agency FB", 28, QtGui.QFont.Bold)

        self.label = QtWidgets.QLabel("设备信息")
        self.label.setFont(title_font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.left_layout.addWidget(self.label)

        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.left_layout.addWidget(self.plainTextEdit)

        button_texts = [
            "获取连接", "任务编辑", "启动任务",
            "中断任务", "生成测试报告", "退出"
        ]
        self.buttons = []
        for text in button_texts:
            btn = QtWidgets.QPushButton(text)
            btn.setMinimumHeight(40)
            self.left_layout.addWidget(btn)
            self.buttons.append(btn)

        self.left_layout.addStretch()

        # 右侧布局
        self.right_layout = QtWidgets.QVBoxLayout()
        self.label_2 = QtWidgets.QLabel("运行信息")
        self.label_2.setFont(title_font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.right_layout.addWidget(self.label_2)

        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit()
        self.right_layout.addWidget(self.plainTextEdit_2)

        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 2)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)