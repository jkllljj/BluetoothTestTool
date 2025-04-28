import json
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DeviceConfig:
    serial: str
    click_coordinates: Tuple[int, int]  # (x, y)


@dataclass
class TaskAction:
    action_type: str
    times: int


@dataclass
class LogConfig:
    file_path: str


class ConfigManager:
    def __init__(self, config_path: str = "../config/config.json"):
        self.config_path = os.path.abspath(config_path)
        self.device: DeviceConfig = None
        self.log: LogConfig = None
        self.tasks: Dict[str, List[TaskAction]] = {}

    def load(self) -> None:
        """加载并解析配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            self.device = DeviceConfig(
                serial=config_data['device']['serial'],
                click_coordinates=(
                    config_data['device']['input']['x'],
                    config_data['device']['input']['y']
                )
            )

            self.log = LogConfig(
                file_path=os.path.expanduser(config_data['log']['file_path'])
            )

            for task_name, actions in config_data['tasks'].items():
                self.tasks[task_name] = [
                    TaskAction(action_type=list(action.keys())[0], times=list(action.values())[0])
                    for action in actions
                ]

        except Exception as e:
            raise ValueError(f"配置文件加载失败: {e}")

    def get_task_actions(self, task_name: str) -> List[TaskAction]:
        """获取指定任务的动作列表"""
        return self.tasks.get(task_name, [])

    def get_device_serial(self) -> str:
        """获取设备序列号"""
        return self.device.serial

    def get_click_coordinates(self) -> Tuple[int, int]:
        """获取点击坐标"""
        return self.device.click_coordinates

    def get_log_directory(self) -> str:
        """获取日志目录（确保目录存在）"""
        os.makedirs(self.log.file_path, exist_ok=True)
        return self.log.file_path
