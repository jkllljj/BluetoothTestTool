# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class TaskSelectorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADB任务选择器")
        self.setFixedSize(450, 320)

        # 设置窗口图标（可选）
        self.setWindowIcon(QtGui.QIcon("icon.png"))  # 请准备相应图标文件

        # 主布局
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题标签
        title_label = QtWidgets.QLabel("选择ADB操作")
        title_label.setFont(QtGui.QFont("Microsoft YaHei", 14, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # 任务类型选择
        self.combo = QtWidgets.QComboBox()
        self.combo.setFont(QtGui.QFont("Microsoft YaHei", 12))
        self.combo.addItems([
            "音量增加 (volume_up)",
            "音量减少 (volume_down)",
            "播放/暂停 (play_pause)",
            "下一曲 (next_track)",
            "上一曲 (previous_track)",
            "重连音箱 (relink)"
        ])
        layout.addWidget(QtWidgets.QLabel("选择操作类型:"))
        layout.addWidget(self.combo)

        # 重复次数选择
        self.spin = QtWidgets.QSpinBox()
        self.spin.setFont(QtGui.QFont("Microsoft YaHei", 12))
        self.spin.setRange(1, 1000)  # 修改最大值为1000
        self.spin.setValue(1)
        self.spin.setSingleStep(5)  # 设置步长为5

        spin_layout = QtWidgets.QHBoxLayout()
        spin_layout.addWidget(QtWidgets.QLabel("重复次数:"))
        spin_layout.addWidget(self.spin)
        spin_layout.addStretch()
        layout.addLayout(spin_layout)

        # 按钮组
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addSpacing(10)
        layout.addWidget(buttons)

        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 200px;
            }
            QPushButton {
                min-width: 80px;
                padding: 8px;
            }
        """)

    def get_selected_task(self):
        """获取选择的任务数据"""
        # 从显示文本中提取动作类型
        action_map = {
            "音量增加 (volume_up)": "volume_up",
            "音量减少 (volume_down)": "volume_down",
            "播放/暂停 (play_pause)": "play_pause",
            "下一曲 (next_track)": "next_track",
            "上一曲 (previous_track)": "previous_track",
            "重连音箱 (relink)": "relink"
        }

        display_text = self.combo.currentText()
        action_type = action_map.get(display_text, display_text)

        return {
            "name": action_type,  # 直接返回动作类型
            "repeat": self.spin.value()
        }


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))
    dialog = TaskSelectorDialog()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        print("选择的任务:", dialog.get_selected_task())
    sys.exit(app.exec_())