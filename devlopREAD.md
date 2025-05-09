# 项目结构

## `src/`
- `__init__.py`  - 包初始化文件，执行包的初始化操作
- `bluetooth_manager.py`  - 蓝牙管理模块，包含连接、断开、获取设备等功能
- `audio_control.py`  - 音频控制模块，负责增减音量、暂停播放、切换歌曲等
- `automation.py`  - 自动化工具模块，负责调用蓝牙管理和音频控制模块，自动执行任务

## `test/`
- `__init__.py`  - 测试包初始化文件
- `test_bluetooth.py`  - 蓝牙管理模块的单元测试
- `test_audio_control.py`  - 音频控制模块的单元测试
- `test_automation.py`  - 自动化工具模块的集成测试

## `logs/`
- `execution_logs.txt`  - 记录工具执行过程中的每次结果

## `config/`
- `settings.py`  - 配置文件，包含蓝牙设备、音频设置等配置

## `report/`
- `test_report.txt`  - 生成的测试报告

后续的改进：
* 把devices序列号和对应设备的input tap坐标保存在config中
* 后续的压测内容也可以通过调整config来进行完成
* 完善log生成和异常处理
* 设备信息的逻辑完善和日志的逻辑完善
