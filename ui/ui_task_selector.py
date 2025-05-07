# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class TaskSelectorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("任务选择器")
        self.setFixedSize(450, 320)

        # 主布局
        layout = QtWidgets.QVBoxLayout(self)

        # 任务类型选择
        self.combo = QtWidgets.QComboBox()
        self.combo.setFont(QtGui.QFont("Arial", 12))
        self.combo.addItems([
            "蓝牙设备扫描",
            "信号强度测试",
            "数据传输测试",
            "设备配对测试"
        ])
        layout.addWidget(self.combo)

        # 重复次数
        self.spin = QtWidgets.QSpinBox()
        self.spin.setFont(QtGui.QFont("Arial", 12))
        self.spin.setRange(1, 100)
        self.spin.setValue(1)
        layout.addWidget(self.spin)

        # 按钮组
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_task(self):
        """获取选择的任务数据"""
        return {
            "name": self.combo.currentText(),
            "repeat": self.spin.value()
        }


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = TaskSelectorDialog()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        print("选择的任务:", dialog.get_selected_task())
    sys.exit(app.exec_())