from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class BaseRotDirButton(QPushButton):
    def __init__(self, direction) -> None:
        super().__init__()
