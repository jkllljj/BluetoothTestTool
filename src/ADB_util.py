import subprocess
import re

class ADB_Utils:
    def __init__(self):
        self.devices = []
        self.state = 0

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
                print(f"执行adb命令出错: {result.stderr}")
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
            return connected_devices

        except Exception as e:
            print(f"获取设备列表时发生异常: {str(e)}")
            return []

    def get_paired_bluetooth_devices(self, device_index=0):
        """获取手机已配对的蓝牙设备名称和MAC地址"""
        if not self.devices:
            print("没有检测到连接的设备")
            return []

        if device_index >= len(self.devices):
            print(f"设备索引 {device_index} 超出范围")
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
                print(f"获取配对设备信息失败: {result.stderr}")
                return []

            # 使用正则表达式提取配对设备信息
            paired_devices = []
            # 改进后的正则表达式，确保捕获每一行设备信息
            pattern = re.compile(
                r"([0-9A-Fa-f:]{17})\s*\[BR/EDR\]\s*(.*?)\n"
            )
            matches = pattern.finditer(result.stdout)

            for match in matches:
                device_address = match.group(1).strip()
                device_name = match.group(2).strip()
                paired_devices.append((device_name, device_address))

            return paired_devices

        except Exception as e:
            print(f"获取配对设备时发生异常: {str(e)}")
            return []

# 使用示例
if __name__ == "__main__":
    adb = ADB_Utils()

    # 获取已连接设备
    adb.get_connected_devices()
    print("已连接的设备序列号:", adb.devices)

    # 获取蓝牙配对设备名称和MAC地址
    paired_devices = adb.get_paired_bluetooth_devices(0)  # 获取第一个设备的已配对设备
    print("\n已配对的蓝牙设备名称和MAC地址:", paired_devices)
