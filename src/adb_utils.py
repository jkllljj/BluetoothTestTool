import subprocess
import time
from idlelib.debugobj import myrepr

from logging_utils import LogUtils
import re

class ADB_Utils:
    def __init__(self, device_serial,click_coordinates):
        self.device_serial = device_serial
        self.logger = LogUtils(f'../logs/{time.time()}.log')  # 使用LogUtils实例
        self.success_count = 0
        self.fail_count = 0
        self.click_coordinates = click_coordinates  # 从配置文件传递过来的坐标

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
            end_time = time.time()
            if result.returncode == 0:
                self.logger.log_command(command, start_time, end_time)
            else:
                self.logger.log_error_with_time(command, result.stderr, start_time, end_time)
        except Exception as e:
            end_time = time.time()
            self.logger.log_error_with_time(command, str(e), start_time, end_time)


    def relink_speaker(self):
        """重新连接/断开蓝牙音箱"""
        self.logger.log_info("开始重新连接/断开音箱")

        if self.is_speaker_connected():
            # 如果音箱已经连接，断开
            self.logger.log_info("音箱已连接，开始断开")
            disconnect_command = f'adb -s {self.device_serial} shell input tap {self.click_coordinates[0]} {self.click_coordinates[1]}'
            subprocess.run(disconnect_command, shell=True)
            time.sleep(2)  # 等待设备响应

            if not self.is_speaker_connected():
                self.logger.log_info("音箱断开成功")
                return "断开成功"
            else:
                self.logger.log_info("音箱断开失败")
                return "断开失败"
        else:
            # 如果音箱未连接，连接
            self.logger.log_info("音箱未连接，开始连接")
            connect_command = f'adb -s {self.device_serial} shell input tap {self.click_coordinates[0]} {self.click_coordinates[1]}'
            subprocess.run(connect_command, shell=True)
            time.sleep(2)  # 等待设备响应

            if self.is_speaker_connected():
                self.logger.log_info("音箱连接成功")
                return "连接成功"
            else:
                self.logger.log_info("音箱连接失败")
                return "连接失败"


    def get_paired_bluetooth_devices(self):
        """获取手机已配对的蓝牙设备名称和MAC地址"""
        if not self.device_serial:
            self.logger.log_info("没有检测到连接的设备")
            return []

        try:
            paired_devices_cmd = f"adb -s {self.device_serial} shell dumpsys bluetooth_manager"
            result = subprocess.run(
                paired_devices_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            if result.returncode != 0:
                self.logger.log_info(f"获取配对设备信息失败: {result.stderr}")
                return []

            # 使用正则表达式提取配对设备信息
            paired_devices = []
            pattern = re.compile(r"AdapterProperties\s*.*?Bonded devices:\s*(.*?)\s*ScanMode", re.DOTALL)
            matches = pattern.search(result.stdout)

            if matches:
                bonded_devices_section = matches.group(1).strip()
                connection_pattern = re.compile(r"([0-9A-Fa-f:]{17})\s*\[BR/EDR\]\s*(.*?)\n")
                connection_matches = connection_pattern.findall(bonded_devices_section)

                for match in connection_matches:
                    device_address = match[0].strip()
                    device_name = match[1].strip()
                    paired_devices.append((device_name, device_address))

            return paired_devices

        except Exception as e:
            self.logger.log_info(f"获取配对设备时发生异常: {str(e)}")
            return []

    def is_speaker_connected(self):
        """检查是否已连接音箱"""
        if not self.device_serial:  # 如果没有设备连接，返回False
            self.logger.log_info("没有检测到连接的设备")
            return False
  # 默认选择第一个设备
        try:
            # 获取蓝牙管理器信息
            connected_device_cmd = f"adb -s {self.device_serial} shell dumpsys bluetooth_manager"
            result = subprocess.run(
                connected_device_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            if result.returncode != 0:
                self.logger.log_info(f"获取蓝牙设备信息失败: {result.stderr}")
                return False

            # 使用正则表达式检查是否有设备连接
            pattern = re.compile(r"ConnectionState: (.*?)\s*Bonded devices:", re.DOTALL)
            matches = pattern.search(result.stdout)

            if matches:
                connection_state = matches.group(1).strip()
                # 判断是否连接
                if "STATE_CONNECTED" in connection_state:
                    self.logger.log_info("已连接音箱设备")
                    return True
                else:
                    self.logger.log_info("未连接音箱设备")
                    return False
            else:
                self.logger.log_info("未找到连接状态信息")
                return False

        except Exception as e:
            self.logger.log_info(f"获取连接音箱状态时发生异常: {str(e)}")
            return False
