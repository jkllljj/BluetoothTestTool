import subprocess
import time
import re
from src.logging_utils import LogUtils

class ADB_Utils:
    def __init__(self, device_serial, click_coordinates):
        self.device_serial = device_serial
        self.click_coordinates = click_coordinates
        self.logger = LogUtils()

    def execute_adb_command(self, command, wait_time=1):
        """统一封装 ADB 命令执行"""
        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10
            )
            end_time = time.time()

            if result.returncode == 0:
                self.logger.log_command(command, start_time, end_time)
                return result.stdout.strip()
            else:
                self.logger.log_error_with_time(command, result.stderr.strip(), start_time, end_time)
                return None
        except Exception as e:
            end_time = time.time()
            self.logger.log_error_with_time(command, str(e), start_time, end_time)
            return None
        finally:
            time.sleep(wait_time)

    def volume_up(self):
        command = f"adb -s {self.device_serial} shell input keyevent KEYCODE_VOLUME_UP"
        self.execute_adb_command(command)

    def volume_down(self):
        command = f"adb -s {self.device_serial} shell input keyevent KEYCODE_VOLUME_DOWN"
        self.execute_adb_command(command)

    def play_pause(self):
        command = f"adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_PLAY_PAUSE"
        self.execute_adb_command(command)

    def next_track(self):
        command = f"adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_NEXT"
        self.execute_adb_command(command)

    def previous_track(self):
        command = f"adb -s {self.device_serial} shell input keyevent KEYCODE_MEDIA_PREVIOUS"
        self.execute_adb_command(command)

    def goto_bluetooth_settings(self):
        """跳转到蓝牙设置界面"""
        command = f"adb -s {self.device_serial} shell am start -a android.settings.BLUETOOTH_SETTINGS"
        self.execute_adb_command(command)
        time.sleep(3)  # 给系统反应时间

    def click_speaker(self):
        """模拟点击蓝牙设备"""
        x, y = self.click_coordinates
        command = f"adb -s {self.device_serial} shell input tap {x} {y}"
        self.execute_adb_command(command)
        time.sleep(2)

    def is_bluetooth_connected(self):
        """判断当前是否有蓝牙设备连接"""
        command = f"adb -s {self.device_serial} shell dumpsys bluetooth_manager"
        output = self.execute_adb_command(command)

        if output is None:
            self.logger.log_info("获取蓝牙设备信息失败")
            return False

        # 尝试找 ConnectionState
        match = re.search(r'ConnectionState:\s*(\w+)', output)
        if match:
            state = match.group(1)
            self.logger.log_info(f"当前蓝牙连接状态: {state}")
            return state == "STATE_CONNECTED"
        else:
            self.logger.log_info("未能找到蓝牙连接状态信息")
            return False

    def relink_speaker(self):
        """执行断开/重连蓝牙设备的操作"""
        self.logger.log_info("开始重新连接/断开音箱")

        if not self.is_bluetooth_connected():
            self.logger.log_info("音箱未连接，开始连接")
            self.goto_bluetooth_settings()
            time.sleep(2)
            self.click_speaker()
            time.sleep(3)

            if self.is_bluetooth_connected():
                self.logger.log_info("音箱连接成功")
            else:
                self.logger.log_info("音箱连接失败")
        else:
            self.logger.log_info("音箱已连接，开始断开")
            self.goto_bluetooth_settings()
            time.sleep(2)
            self.click_speaker()
            time.sleep(3)

            if not self.is_bluetooth_connected():
                self.logger.log_info("音箱断开成功")
            else:
                self.logger.log_info("音箱断开失败")
