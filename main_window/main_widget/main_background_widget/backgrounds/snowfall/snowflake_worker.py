from PyQt6.QtCore import QThread
from .snowflake_manager import SnowflakeManager


class SnowflakeThread(QThread):
    def __init__(self, manager: SnowflakeManager):
        super().__init__()
        self.manager = manager

    def run(self):
        self.manager.animate_snowflakes()
