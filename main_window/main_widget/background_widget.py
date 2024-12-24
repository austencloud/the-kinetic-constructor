# background_widget.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QSize

import logging
if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
from PyQt6.QtWidgets import QSizePolicy


class BackgroundWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.setStyleSheet("background: transparent;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.show()

    def paintEvent(self, event):
        logging.debug("BackgroundWidget.paintEvent called")
        # print(f"{self.__class__.__name__} paintEvent called")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.main_widget.background:
            self.main_widget.background.paint_background(self, painter)
        else:
            logging.warning("No background set in main_widget.background")
        painter.end()
        print("BackgroundWidget.paintEvent done")

    def resizeEvent(self, event):
        self.resize(self.main_widget.size())
        super().resizeEvent(event)
