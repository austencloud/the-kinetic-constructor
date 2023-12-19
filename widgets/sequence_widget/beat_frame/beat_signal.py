from PyQt6.QtCore import pyqtSignal, QObject

from objects.motion import Motion
from objects.pictograph.pictograph import Pictograph


class BeatSignal(QObject):
    signal = pyqtSignal(Pictograph)
