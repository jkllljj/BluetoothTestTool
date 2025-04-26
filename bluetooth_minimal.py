import logging
import subprocess
import time
from datetime import datetime


class BluetoothMinimal:
    def __init__(self):
        self.check_adb()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/bluetooth_test.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BluetoothTest')

        # 记录测试开始信息
        self.logger.info("=" * 50)
        self.logger.info("蓝牙重连测试开始")
        self.logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 50)

    def check_adb(self):
        """检查ADB连接"""
        subprocess.run("adb start-server", shell=True)
        time.sleep(5)
        result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
        if result.stdout.strip() == 'List of devices attached':
            raise Exception("未检测到已授权的ADB设备")

    def reboot_bluetooth(self):
        """"""
        #重启蓝牙
        subprocess.run(f"adb shell svc bluetooth disable", shell=True)
        time.sleep(2)  #
        subprocess.run(f"adb shell svc bluetooth enable", shell=True)
        time.sleep(2)

    #该功能被禁用了，等后续再实现
    # def connect_speaker(self, mac):
    #     """连接蓝牙音箱（需已配对）"""
    #     # 方法1：直接通过A2DP协议连接，小米无法实现此功能被禁用了
    #     subprocess.run(
    #         f"adb shell am start -a android.bluetooth.a2dp.profile.action.CONNECT --es device {mac}",
    #         shell=True
    #     )

    # 方法2：备用方案 - 模拟UI点击（兼容性不够好）
    def _ui_connect(self, mac):
        """通过UI操作连接（需校准坐标）"""
        subprocess.run("adb shell am start -a android.settings.BLUETOOTH_SETTINGS", shell=True)
        time.sleep(4)
        # subprocess.run(f"adb shell input tap 160 880", shell=True)  # 点击连接按钮
        subprocess.run(f"adb shell input tap 300 900", shell=True)

    def is_connected(self, mac):
        """检查连接状态"""
        time.sleep(5)
        result = subprocess.run(
            "adb shell dumpsys bluetooth_manager | findstr \"state=Connected\"",
            shell=True, capture_output=True, text=True
        )
        return "state=connected" in result.stdout.lower()

    def relink_bluetooth(self, times):
        count = 0
        success_count = 0
        start_time = time.time()
        while count < times:
            count += 1
            #获取时间
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                # 点击断开
                subprocess.run("adb shell input tap 300 900", shell=True, check=True)
                time.sleep(2)

                # 点击连接
                subprocess.run("adb shell input tap 300 900", shell=True, check=True)
                time.sleep(2)

                # 判断是否连接成功
                if self.is_connected(''):
                    success_count += 1
                    log_msg = f"第 {count}/{times} 次 - 成功 - {current_time}"
                    self.logger.info(log_msg)
                else:
                    log_msg = f"第 {count}/{times} 次 - 失败 - {current_time}"
                    self.logger.error(log_msg)
                    break

            except subprocess.CalledProcessError as e:
                self.logger.error(f"第 {count} 次执行ADB命令失败: {str(e)}")
                break
            except Exception as e:
                self.logger.error(f"第 {count} 次发生未知错误: {str(e)}")
                break

        # 测试结束统计
        end_time = time.time()
        duration = end_time - start_time
        success_rate = (success_count / times) * 100 if times > 0 else 0

        self.logger.info("=" * 50)
        self.logger.info("测试结果统计:")
        self.logger.info(f"总执行次数: {count}")
        self.logger.info(f"成功次数: {success_count}")
        self.logger.info(f"失败次数: {count - success_count}")
        self.logger.info(f"成功率: {success_rate:.2f}%")
        self.logger.info(f"总耗时: {duration:.2f} 秒")
        self.logger.info(f"平均每次耗时: {duration / count:.2f} 秒" if count > 0 else "N/A")
        self.logger.info("=" * 50)

        return success_count == times




if __name__ == "__main__":
    bt = BluetoothMinimal()
    # 测试流程
    #SPEAKER_MAC = "E826CFC7FBEC"  # 替换为音箱实际MAC
    print("1. 重启蓝牙...")
    bt.reboot_bluetooth()
    print("2. 连接音箱...")
    #Mac链接暂无法实现（小米）等后续改进，目前先使用UI连接
    #bt.connect_speaker(SPEAKER_MAC)
    #通过UI连接音箱
    bt._ui_connect('')
    time.sleep(5)  # 等待连接完成
    print("3. 验证连接...")
    if bt.is_connected(''):
        print("音箱连接成功！")
        #进行重连n次
        bt.relink_bluetooth(50)
    else:
        print("连接失败，请检查：\n- 音箱是否已配对\n- MAC地址是否正确")
