from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap

class ImageLoaderSignals(QObject):
    finished = pyqtSignal(str, QPixmap)

class ImageLoaderRunnable(QRunnable):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.signals = ImageLoaderSignals()

    @pyqtSlot()
    def run(self):
        pixmap = QPixmap(self.image_path)
        self.signals.finished.emit(self.image_path, pixmap)