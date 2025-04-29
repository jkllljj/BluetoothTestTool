import time
from src.config_manager import ConfigManager
from src.adb_utils import ADB_Utils
from src.logging_utils import LogUtils

class TaskExecutor:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = LogUtils()
        self.success_count = 0
        self.fail_count = 0

    def execute_all_tasks(self):
        """执行所有配置的任务"""
        device_serial = self.config.get_device_serial()
        click_coordinates = self.config.get_click_coordinates()
        adb_utils = ADB_Utils(device_serial, click_coordinates)

        device_info = f"设备序列号: {device_serial}, 点击坐标: {click_coordinates}"
        self.logger.log_info(f"任务执行开始\n{device_info}\n")

        # 【新增】先确保蓝牙音箱是连接状态
        self.logger.log_info("开始检测蓝牙设备连接状态...")
        if not adb_utils.is_bluetooth_connected():
            self.logger.log_info("检测到蓝牙未连接，尝试进行连接...")
            adb_utils.goto_bluetooth_settings()  # 跳转到蓝牙设置
            time.sleep(3)  # 等页面稳定

            adb_utils.click_speaker()  # 尝试点击连接
            time.sleep(3)

            # 再次确认连接状态
            if not adb_utils.is_bluetooth_connected():
                self.logger.log_error("蓝牙设备连接失败，停止任务执行")
                return
            else:
                self.logger.log_info("蓝牙设备连接成功，开始执行任务")
        else:
            self.logger.log_info("蓝牙设备已连接，直接开始执行任务")

        # 【正常任务流程】
        for task_name, actions in self.config.tasks.items():
            self.logger.log_info(f"\n开始执行任务: {task_name}")
            for action in actions:
                self._execute_action(action)

        self.logger.log_info(f"\n任务执行结束\n成功操作: {self.success_count} 次，失败操作: {self.fail_count} 次")

    def _execute_action(self, action):
        """执行单个动作"""
        device_serial = self.config.get_device_serial()
        click_coordinates = self.config.get_click_coordinates()
        adb_utils = ADB_Utils(device_serial, click_coordinates)

        for i in range(action.times):
            try:
                # 显示执行进度
                progress = f"{i + 1}/{action.times}"
                self.logger.log_info(f"执行进度: {progress}")

                # 👉【在执行每个动作前，强制检查蓝牙是否连接】
                if not adb_utils.is_bluetooth_connected():
                    self.logger.log_info("检测到蓝牙未连接，开始尝试连接音箱...")
                    adb_utils.relink_speaker()

                # ✅ 然后才继续正常执行任务
                if action.action_type == "volume_up":
                    adb_utils.volume_up()
                elif action.action_type == "volume_down":
                    adb_utils.volume_down()
                elif action.action_type == "play_pause":
                    adb_utils.play_pause()
                elif action.action_type == "next_track":
                    adb_utils.next_track()
                elif action.action_type == "previous_track":
                    adb_utils.previous_track()
                elif action.action_type == "relink":
                    adb_utils.relink_speaker()
                else:
                    self.logger.log_warning(f"未知的动作类型: {action.action_type}")

                # 操作间隔
                time.sleep(2)
                self.success_count += 1  # 成功计数

            except Exception as e:
                self.fail_count += 1  # 失败计数
                self.logger.log_error(f"{action.action_type} 执行失败: {str(e)}")
                continue  # 继续执行下一个操作
