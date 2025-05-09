import time
from src.config_manager import ConfigManager
from src.adb_utils import ADB_Utils


class TaskExecutor:
    def __init__(self, config: ConfigManager, log_signal):
        self.config = config
        self.log_signal = log_signal
        self.success_count = 0
        self.fail_count = 0

    def log(self, message, is_error=False):
        """线程安全的日志记录"""
        prefix = "[ERROR]" if is_error else "[INFO]"
        self.log_signal.emit(f"{prefix} {message}")

    def execute_all_tasks(self):
        """执行所有配置的任务"""
        device_serial = self.config.get_device_serial()
        click_coordinates = self.config.get_click_coordinates()
        adb_utils = ADB_Utils(device_serial, click_coordinates)

        self.log(f"设备序列号: {device_serial}")
        self.log(f"点击坐标: {click_coordinates}")

        # 检查蓝牙连接
        if not self._ensure_bluetooth_connected(adb_utils):
            self.log("蓝牙设备连接失败，终止任务", is_error=True)
            return

        # 执行配置的任务
        for task_name, actions in self.config.tasks.items():
            self.log(f"\n>> 开始任务: {task_name}")
            for action in actions:
                self._execute_action(adb_utils, action)

        self.log(f"\n=== 任务统计 ===")
        self.log(f"成功操作: {self.success_count} 次")
        self.log(f"失败操作: {self.fail_count} 次")

    def _ensure_bluetooth_connected(self, adb_utils):
        """确保蓝牙设备已连接"""
        self.log("检查蓝牙连接状态...")
        if not adb_utils.is_bluetooth_connected():
            self.log("蓝牙未连接，尝试连接...")
            adb_utils.relink_speaker()
            return adb_utils.is_bluetooth_connected()
        return True

    def _execute_action(self, adb_utils, action):
        """执行单个动作"""
        action_type = action.action_type
        times = action.times

        for i in range(times):
            try:
                self.log(f"执行 {action_type} ({i + 1}/{times})")

                # 检查蓝牙连接
                if not adb_utils.is_bluetooth_connected():
                    self.log("蓝牙断开，尝试重新连接...")
                    adb_utils.relink_speaker()

                # 执行动作
                if action_type == "volume_up":
                    adb_utils.volume_up()
                elif action_type == "volume_down":
                    adb_utils.volume_down()
                elif action_type == "play_pause":
                    adb_utils.play_pause()
                elif action_type == "next_track":
                    adb_utils.next_track()
                elif action_type == "previous_track":
                    adb_utils.previous_track()
                elif action_type == "relink":
                    adb_utils.relink_speaker()
                else:
                    self.log(f"未知动作类型: {action_type}", is_error=True)

                time.sleep(1.8)  # 操作间隔
                self.success_count += 1
            except Exception as e:
                self.fail_count += 1
                self.log(f"{action_type} 执行失败: {str(e)}", is_error=True)