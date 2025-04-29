import logging
import os
from datetime import datetime


class LogUtils:
    _logger = None  # 类变量，全局共享

    def __init__(self, log_file=None):
        """初始化日志系统"""
        if LogUtils._logger is not None:
            self.logger = LogUtils._logger
            return

        # 第一次创建logger
        logger = logging.getLogger('BluetoothTestLogger')
        logger.setLevel(logging.INFO)
        logger.propagate = False  # 防止日志冒泡到root导致重复打印

        if not log_file:
            log_dir = "../logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # 文件输出
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger
        LogUtils._logger = logger  # 保存为类变量，全局唯一

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_command(self, command, start_time, end_time):
        duration = end_time - start_time
        self.logger.info(f"执行ADB命令: {command}，耗时: {duration:.2f}秒")

    def log_error_with_time(self, command, error_message, start_time, end_time):
        duration = end_time - start_time
        self.logger.error(f"执行ADB命令: {command} 出错，错误信息: {error_message}，耗时: {duration:.2f}秒")
