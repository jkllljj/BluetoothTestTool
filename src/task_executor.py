import time
from src.config_manager import ConfigManager
from src.adb_utils import ADB_Utils
from src.logging_utils import LogUtils


class TaskExecutor:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = LogUtils()  # 创建日志记录实例
        self.success_count = 0
        self.fail_count = 0

    def execute_all_tasks(self):
        """执行所有配置的任务"""
        # 获取设备信息
        device_serial = self.config.get_device_serial()
        device_info = f"设备序列号: {device_serial}, 点击坐标: {self.config.get_click_coordinates()}"

        # 打印日志头部，记录设备信息和任务内容
        self.logger.log_info(f"任务执行开始\n{device_info}\n")

        # 执行每个任务
        for task_name, actions in self.config.tasks.items():
            self.logger.log_info(f"\n开始执行任务: {task_name}")
            for action in actions:
                self._execute_action(action)

        # 记录任务执行结束时的统计信息
        self.logger.log_info(f"\n任务执行结束\n成功操作: {self.success_count} 次，失败操作: {self.fail_count} 次")

    def _execute_action(self, action):
        """执行单个动作"""
        device_serial = self.config.get_device_serial()
        click_coordinates = self.config.get_click_coordinates()
        adb_utils = ADB_Utils(device_serial,click_coordinates)

        for i in range(action.times):
            try:
                # 显示执行进度
                progress = f"{i + 1}/{action.times}"
                self.logger.log_info(f"执行进度: {progress}")

                # 根据不同的操作类型调用相应的函数
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
                elif action.action_type == "relink":  # 重连函数要针对不同机型做调整
                    adb_utils.relink_speaker()

                # 操作间隔
                time.sleep(2)
                self.success_count += 1  # 成功计数
            except Exception as e:
                self.fail_count += 1  # 失败计数
                self.logger.log_error(f"{action.action_type} 执行失败: {str(e)}")
                continue  # 继续执行下一个操作

    def log_task_summary(self):
        """记录任务执行总结"""
        self.logger.log_info(f"\n总结:\n成功操作: {self.success_count} 次\n失败操作: {self.fail_count} 次")
