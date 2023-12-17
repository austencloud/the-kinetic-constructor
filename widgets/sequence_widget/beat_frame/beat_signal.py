from PyQt6.QtCore import pyqtSignal, QObject

from objects.motion import Motion


class BeatSignal(QObject):
    signal = pyqtSignal(Motion, Motion)
