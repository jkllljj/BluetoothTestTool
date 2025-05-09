# -*- coding: utf-8 -*-
import json
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui_mainWindow import Ui_MainWindow
from ui_task_editor import TaskEditorWindow
from src.config_manager import ConfigManager
from src.task_executor import TaskExecutor
from threading import Thread


class MainApplication(QtWidgets.QMainWindow):
    log_signal = QtCore.pyqtSignal(str)  # 用于线程安全的日志更新

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.log_signal.connect(self.update_log)

        # 初始化配置目录
        self.config_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../config'))
        os.makedirs(self.config_dir, exist_ok=True)

        # 初始化配置
        self.config = ConfigManager(
            config_path=os.path.join(self.config_dir, 'config.json')
        )
        try:
            self.config.load()
        except Exception as e:
            self.log_signal.emit(f"[ERROR] 加载配置失败: {str(e)}")
            QMessageBox.critical(self, "配置错误", f"加载配置失败: {str(e)}")

        # 连接按钮信号
        self.ui.buttons[0].clicked.connect(self.check_adb_connection)
        self.ui.buttons[1].clicked.connect(self.open_task_editor)
        self.ui.buttons[2].clicked.connect(self.execute_task)
        self.ui.buttons[3].clicked.connect(self.interrupt_task)
        self.ui.buttons[4].clicked.connect(self.generate_report)
        self.ui.buttons[5].clicked.connect(self.close)

        # 状态初始化
        self.is_task_running = False
        self.task_thread = None
        self.update_device_info()

    def update_log(self, message):
        """线程安全的日志更新"""
        self.ui.plainTextEdit_2.appendPlainText(message)
        QtCore.QCoreApplication.processEvents()

    def update_device_info(self):
        """更新设备信息显示"""
        info = f"""设备控制面板 v1.1
-------------------
状态: {self.get_connection_status()}
序列号: {self.config.get_device_serial()}
点击坐标: {self.config.get_click_coordinates()}
任务: {"运行中" if self.is_task_running else "准备就绪"}"""
        self.ui.plainTextEdit.setPlainText(info)

    def get_connection_status(self):
        """获取连接状态文本"""
        return "已连接" if self.config.get_device_serial() else "未连接"

    def check_adb_connection(self):
        """检查ADB连接"""
        self.log_signal.emit("\n=== 检查ADB连接 ===")
        try:
            from src.adb_utils import ADB_Utils
            adb = ADB_Utils(self.config.get_device_serial(), self.config.get_click_coordinates())
            output = adb.execute_adb_command("adb devices")
            if output and self.config.get_device_serial() in output:
                self.log_signal.emit(f"设备 {self.config.get_device_serial()} 已连接")
            else:
                self.log_signal.emit("未检测到设备，请检查连接")
        except Exception as e:
            self.log_signal.emit(f"[ERROR] 检查连接失败: {str(e)}")
        self.update_device_info()

    def open_task_editor(self):
        """打开任务编辑器"""
        self.task_editor = TaskEditorWindow(self)
        self.task_editor.show()

    def execute_task(self):
        """执行ADB任务"""
        if self.is_task_running:
            QMessageBox.warning(self, "警告", "当前有任务正在执行")
            return

        self.log_signal.emit("\n=== 开始执行任务 ===")
        self.is_task_running = True
        self.update_device_info()

        def _run_tasks():
            try:
                executor = TaskExecutor(self.config, self.log_signal)
                executor.execute_all_tasks()
                self.log_signal.emit("\n=== 所有任务执行完成 ===")
            except Exception as e:
                self.log_signal.emit(f"[ERROR] 任务执行异常: {str(e)}")
            finally:
                self.is_task_running = False
                self.update_device_info()

        self.task_thread = Thread(target=_run_tasks)
        self.task_thread.start()

    def interrupt_task(self):
        """中断任务"""
        if not self.is_task_running:
            QMessageBox.warning(self, "提示", "当前没有运行中的任务")
            return

        reply = QMessageBox.question(
            self, "确认",
            "确定要中断当前任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.is_task_running = False
            self.log_signal.emit("\n=== 任务已中断 ===")
            self.update_device_info()

    def generate_report(self):
        """生成测试报告"""
        log_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../logs'))
        os.makedirs(log_dir, exist_ok=True)

        report_path = os.path.join(log_dir, "task_report.log")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(self.ui.plainTextEdit_2.toPlainText())
            QMessageBox.information(self, "成功", f"报告已保存到:\n{report_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成报告失败:\n{str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())