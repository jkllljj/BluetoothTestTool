import unittest

from src.adb_utils import ADB_Utils
from src.logging_utils import LogUtils


class TestADBUtils(unittest.TestCase):
    def test_relink_speaker(self):
        device_serial = "your_device_serial"
        logger = LogUtils("test_log.log")
        click_coordinates = (400, 900)

        adb_utils = ADB_Utils(device_serial, logger, click_coordinates)

        # 调用 relink_speaker 测试连接或断开操作
        result = adb_utils.relink_speaker()

        # 断言是否返回正确的结果
        self.assertIn(result, ["连接成功", "断开成功"])

    def test_is_speaker_connected(self):
        device_serial = "your_device_serial"
        logger = LogUtils("test_log.log")
        click_coordinates = (400, 900)

        adb_utils = ADB_Utils(device_serial, logger, click_coordinates)

        # 测试是否能正确判断音箱连接状态
        self.assertIsInstance(adb_utils.is_speaker_connected(), bool)


if __name__ == "__main__":
    unittest.main()
