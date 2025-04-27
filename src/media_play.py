import subprocess
import time
from datetime import datetime

from logging_utils import LogUtils

class MediaControl:
    def __init__(self, device_serial):
        self.device_serial = device_serial
        self.logger = LogUtils(f'../logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')  # 使用LogUtils实例
        self.success_count = 0
        self.fail_count = 0

    def volume_up(self):
        """增大音量"""
        command = f'adb -s {self.device_serial} shell input keyevent KEYCODE_VOLUME_UP'
        self.execute_command(command)

    def volume_down(self):
        """减小音量"""
        command = f'adb -s {self.device_serial} shell input keyevent KEYCODE_VOLUME_DOWN'
        self.execute_command(command)

    def play_pause(self):
        """播放/暂停"""
        command = f'adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_PLAY_PAUSE'
        self.execute_command(command)

    def next_track(self):
        """切换到下一首歌曲"""
        command = f'adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_NEXT'
        self.execute_command(command)

    def previous_track(self):
        """切换到上一首歌曲"""
        command = f'adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_PREVIOUS'
        self.execute_command(command)

    def execute_command(self, command):
        """执行 adb 命令，并捕获输出和错误"""
        start_time = time.time()
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, encoding='utf-8'
            )
            if result.returncode == 0:
                end_time = time.time()
                self.logger.log_command(command, start_time, end_time)
                self.success_count += 1
            else:
                end_time = time.time()
                self.logger.log_error_with_time(command, result.stderr, start_time, end_time)
                self.fail_count += 1
        except Exception as e:
            end_time = time.time()
            self.logger.log_error_with_time(command, str(e), start_time, end_time)
            self.fail_count += 1

    def test_media_operations(self, num_operations=10):
        """执行多次压测操作"""
        self.logger.log_info("开始进行多媒体压测")

        for i in range(num_operations):
            try:
                progress = f"{i + 1}/{num_operations}"
                self.logger.log_info(f"执行进度: {progress}")

                # 随机选择操作进行压测
                operation = self.choose_random_operation()
                self.logger.log_info(f"执行操作: {operation}")

                if operation == "volume_up":
                    self.volume_up()
                elif operation == "volume_down":
                    self.volume_down()
                elif operation == "play_pause":
                    self.play_pause()
                elif operation == "next_track":
                    self.next_track()
                elif operation == "previous_track":
                    self.previous_track()

                # 增加 sleep 来模拟每次操作之间的间隔
                time.sleep(2)

            except Exception as e:
                self.logger.log_error(f"操作失败: {str(e)}")
                continue

        self.logger.log_info(f"压测完成，总共成功 {self.success_count} 次，失败 {self.fail_count} 次。")

    def choose_random_operation(self):
        """随机选择操作，可以根据需要修改选择的方式"""
        import random
        operations = ["volume_up", "volume_down", "play_pause", "next_track", "previous_track"]
        return random.choice(operations)

    def stress_test(self, command):
        pass
# 使用示例
if __name__ == "__main__":
    # 假设设备序列号是 "R5CW505P3RK"
    device_serial = "b67c9d18"
    media_control = MediaControl(device_serial)

    # 执行多次操作并生成日志
    media_control.test_media_operations(num_operations=10)
