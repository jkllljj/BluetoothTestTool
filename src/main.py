from src.config_manager import ConfigManager
from src.task_executor import TaskExecutor

def main():
    config = ConfigManager()
    config.load()

    executor = TaskExecutor(config)
    executor.execute_all_tasks()

if __name__ == "__main__":
    main()
