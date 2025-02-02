import json
import random
from PyQt6.QtCore import Qt, QTimer, QThreadPool, QRunnable, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import QOpenGLWindow


class SnowflakeConfigManager(QObject):
    config_updated = pyqtSignal(dict)

    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as file:
                self.config = json.load(file)
                self.config_updated.emit(self.config)
        except FileNotFoundError:
            self.config = {}

    def update_config(self, new_config):
        with open(self.config_path, "w") as file:
            json.dump(new_config, file, indent=4)
        self.load_config()
