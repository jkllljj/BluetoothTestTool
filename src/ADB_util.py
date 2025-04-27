import datetime
import subprocess
import re
import time
from logging_utils import LogUtils



class ADB_Utils:
    def __init__(self):
        self.devices = []
        self.state = 0
        self.logger = LogUtils(f'../logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')  # 使用LogUtils实例
        self.success_count = 0
        self.fail_count = 0
        self.total_start_time = time.time()

    def get_connected_devices(self):
        """获取已连接的ADB设备序列号列表"""
        try:
            result = subprocess.run(
                "adb devices -l",
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            # 检查命令是否执行成功
            if result.returncode != 0:
                self.logger.log_info(f"执行adb命令出错: {result.stderr}")
                return []

            # 解析输出
            lines = result.stdout.strip().split('\n')[1:]  # 跳过第一行标题
            connected_devices = []

            for line in lines:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    # 提取设备序列号（通常是第一个字段）
                    device_serial = parts[0]
                    connected_devices.append(device_serial)

            self.devices = connected_devices
            self.logger.log_info(f"已连接的设备序列号: {connected_devices}")
            return connected_devices

        except Exception as e:
            self.logger.log_info(f"获取设备列表时发生异常: {str(e)}")
            return []

    def simulate_click_connect(self, device_index=0, times=0):
        """通过模拟点击的方式来进行蓝牙连接断开"""
        if not self.devices:  # 如果没有设备连接，直接返回
            self.logger.log_info("没有已连接的设备，无法执行操作")
            return

        device_serial = self.devices[device_index]
        self.logger.log_info(f"开始执行模拟点击操作，设备序列号: {device_serial}")
        self.logger.log_info(f"执行次数: {times}")

        # 打印日志头，包含设备信息和执行次数
        paired_devices = self.get_paired_bluetooth_devices(device_index)
        self.logger.log_info("蓝牙配对设备信息:")
        goto_bluetooth_cmd = f'adb -s {device_serial} shell am start -a android.settings.BLUETOOTH_SETTINGS'
        for device_name, device_address in paired_devices:
            self.logger.log_info(f"设备名称: {device_name}, MAC 地址: {device_address}")

        current = 0
        while current < times:
            try:
                # 显示进度
                progress = f"{current + 1}/{times}"
                self.logger.log_info(f"执行进度: {progress}")

                # 获取到要操作的手机序列号
                # 进入蓝牙连接页面
                start_time = time.time()

                result = subprocess.run(
                    goto_bluetooth_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'  # 忽略编码错误
                )

                # 等待直到命令执行完成
                result.check_returncode()

                # 先判断是否连接设备
                if self.state == 1:  # 连接成功，开始断开，记录断开时间
                    self.logger.log_info(f'{progress}: 有设备连接,开始断开')
                    self.sumsung_click(device_serial, action="断开")
                else:  # 未连接，开始连接，记录连接时间
                    self.logger.log_info(f'{progress}: 无设备连接,开始连接')
                    self.sumsung_click(device_serial, action="连接")

                # 增加sleep时间，确保手机有足够的时间响应
                self.wait_for_device_response()

                end_time = time.time()
                self.logger.log_command(goto_bluetooth_cmd, start_time, end_time)

                # 统计成功的操作
                self.success_count += 1
                current += 1

            except subprocess.CalledProcessError as e:
                end_time = time.time()
                self.logger.log_error_with_time(goto_bluetooth_cmd, f"ADB命令失败: {str(e)}", start_time, end_time)
                self.fail_count += 1

        # 打印日志尾，包含统计信息
        total_end_time = time.time()
        total_execution_time = total_end_time - self.total_start_time
        self.logger.log_info(f"总共执行 {times} 次操作，其中成功 {self.success_count} 次，失败 {self.fail_count} 次。")
        self.logger.log_info(f"总执行时间: {total_execution_time:.2f} 秒")

    def wait_for_device_response(self):
        """确保设备有足够的时间响应操作"""
        # 增加等待时间，确保设备响应完毕
        time.sleep(4)

    def sumsung_click(self, device_serial, action):
        """模拟点击连接或断开设备"""
        start_time = time.time()
        self.logger.log_info(f"模拟点击 {action} 设备, 设备序列号: {device_serial}")

        # 调整点击位置，确保点击操作精准
        if action == "连接":
            subprocess.run(f'adb -s {device_serial} shell input tap 400 900')
            time.sleep(1)
        elif action == "断开":
            subprocess.run(f'adb -s {device_serial} shell input tap 400 900')
            time.sleep(1)
        end_time = time.time()
        self.logger.log_command(f"点击 {action} 设备", start_time, end_time)

    def get_paired_bluetooth_devices(self, device_index=0):
        """获取手机已配对的蓝牙设备名称和MAC地址"""
        if not self.devices:
            self.logger.log_info("没有检测到连接的设备")
            return []

        if device_index >= len(self.devices):
            self.logger.log_info(f"设备索引 {device_index} 超出范围")
            return []

        device_serial = self.devices[device_index]

        try:
            # 获取已配对设备的详细信息
            paired_devices_cmd = f"adb -s {device_serial} shell dumpsys bluetooth_manager"
            result = subprocess.run(
                paired_devices_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'  # 忽略编码错误
            )

            # 检查命令是否成功执行
            if result.returncode != 0:
                self.logger.log_info(f"获取配对设备信息失败: {result.stderr}")
                return []

            # 使用正则表达式提取配对设备信息
            paired_devices = []
            # 改进后的正则表达式，确保捕获每一行设备信息，专注于AdapterProperties下的内容
            pattern = re.compile(
                r"AdapterProperties\s*.*?Bonded devices:\s*(.*?)\s*ScanMode", re.DOTALL
            )
            matches = pattern.search(result.stdout)

            if matches:
                bonded_devices_section = matches.group(1).strip()
                connection_pattern = re.compile(
                    r"([0-9A-Fa-f:]{17})\s*\[BR/EDR\]\s*(.*?)\n"
                )
                connection_matches = connection_pattern.findall(bonded_devices_section)

                for match in connection_matches:
                    device_address = match[0].strip()
                    device_name = match[1].strip()
                    paired_devices.append((device_name, device_address))

            return paired_devices

        except Exception as e:
            self.logger.log_info(f"获取配对设备时发生异常: {str(e)}")
            return []

    def get_connected_bluetooth_device(self, device_index=0):
        """获取当前已连接的蓝牙设备名称和MAC地址"""
        if not self.devices:
            self.logger.log_info("没有检测到连接的设备")
            return None

        if device_index >= len(self.devices):
            self.logger.log_info(f"设备索引 {device_index} 超出范围")
            return None

        device_serial = self.devices[device_index]

        try:
            # 获取当前连接的蓝牙设备信息
            connected_device_cmd = f"adb -s {device_serial} shell dumpsys bluetooth_manager"
            result = subprocess.run(
                connected_device_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'  # 忽略编码错误
            )

            # 检查命令是否成功执行
            if result.returncode != 0:
                self.logger.log_info(f"获取蓝牙连接信息失败: {result.stderr}")
                return None

            # 使用正则表达式提取连接设备信息
            connected_device = None
            pattern = re.compile(
                r"AdapterProperties\s*.*?ConnectionState: (.*?)\s*Bonded devices:", re.DOTALL
            )
            matches = pattern.search(result.stdout)

            if matches:
                connection_state = matches.group(1).strip()
                # 判断是否已连接
                if "STATE_CONNECTED" in connection_state:
                    connected_device = "已连接"
                    self.state = 1
                else:
                    self.state = 0

            return connected_device

        except Exception as e:
            self.logger.log_info(f"获取已连接蓝牙设备时发生异常: {str(e)}")
            return None


# 使用示例
if __name__ == "__main__":
    adb = ADB_Utils()

    # 获取已连接设备
    adb.get_connected_devices()
    paired = adb.get_paired_bluetooth_devices()
    adb.simulate_click_connect(device_index=0, times=10)
