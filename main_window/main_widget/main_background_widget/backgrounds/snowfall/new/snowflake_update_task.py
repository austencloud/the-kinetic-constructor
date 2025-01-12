import json
import random
from PyQt6.QtCore import Qt, QTimer, QThreadPool, QRunnable, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtOpenGL import QOpenGLWindow

from main_window.main_widget.main_background_widget.backgrounds.snowfall.snowflake import Snowflake
class SnowflakeUpdateTask(QRunnable):
    def __init__(self, snowflakes: list[Snowflake]):
        super().__init__()
        self.snowflakes = snowflakes

    def run(self):
        for snowflake in self.snowflakes:
            snowflake.update_position()
