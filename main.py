import subprocess
import time
from src.ADB_util import ADB_Utils
from src.media_play import MediaControl
from src.logging_utils import LogUtils

def main():
    # 初始化日志系统
    logger = LogUtils(f'../logs/{time.time()}.log')  # 使用LogUtils实例
    logger.log_info("程序启动...")

    # 获取已连接设备
    adb = ADB_Utils()
    connected_devices = adb.get_connected_devices()

    if not connected_devices:
        logger.log_info("没有检测到已连接的设备")
        return

    logger.log_info(f"已连接的设备序列号: {connected_devices}")

    # 选择第一个设备（可以根据需要修改选择逻辑）
    device_serial = connected_devices[0]

    # 创建 MediaControl 实例
    media_control = MediaControl(device_serial)

    # 打印蓝牙配对设备信息
    paired_devices = adb.get_paired_bluetooth_devices()
    logger.log_info("蓝牙配对设备信息:")
    for device_name, device_address in paired_devices:
        logger.log_info(f"设备名称: {device_name}, MAC 地址: {device_address}")

    # 执行多媒体操作压测
    media_control.test_media_operations(num_operations=10)

    # 结束日志记录
    logger.log_info("程序结束...")

if __name__ == "__main__":
    main()
