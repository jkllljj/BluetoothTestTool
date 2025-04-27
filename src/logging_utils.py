import logging
import time
from datetime import datetime


class LogUtils:
    def __init__(self, log_file=None):
        """初始化日志系统，设置日志格式和文件输出"""
        if log_file is None:
            log_file = f"../logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"  # 生成按日期区分的日志文件名

        # 创建一个日志记录器
        self.logger = logging.getLogger('ADB_Automation')
        self.logger.setLevel(logging.INFO)

        # 创建一个日志文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 添加处理器到日志记录器
        self.logger.addHandler(file_handler)

        # 同时打印日志到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        """记录普通信息"""
        self.logger.info(message)

    def log_error(self, message):
        """记录错误信息"""
        self.logger.error(message)

    def log_warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def log_command(self, command, start_time, end_time):
        """记录ADB命令及其执行时间"""
        execution_time = end_time - start_time
        self.log_info(f"执行ADB命令: {command}，耗时: {execution_time:.2f}秒")

    def log_status(self, status_message):
        """记录状态信息（例如连接、断开操作）"""
        self.log_info(status_message)

    def log_error_with_time(self, command, error_message, start_time, end_time):
        """记录错误的ADB命令及其执行时间"""
        execution_time = end_time - start_time
        self.log_error(f"执行ADB命令: {command} 出错，错误信息: {error_message}，耗时: {execution_time:.2f}秒")


# 用法示例
if __name__ == "__main__":
    log_utils = LogUtils()

    # 记录程序启动
    log_utils.log_info("程序启动...")

    # 记录一个命令的执行
    adb_command = "adb devices -l"
    start_time = time.time()
    try:
        # 假设此处运行某个ADB命令
        1 / 0  # 故意制造异常
        time.sleep(1)  # 模拟执行时间
        end_time = time.time()
        log_utils.log_command(adb_command, start_time, end_time)
    except Exception as e:
        end_time = time.time()
        log_utils.log_error_with_time(adb_command, str(e), start_time, end_time)

    # 记录设备连接状态
    log_utils.log_status("设备连接成功，开始进行蓝牙操作")

    # 记录程序结束
    log_utils.log_info("程序结束...")
