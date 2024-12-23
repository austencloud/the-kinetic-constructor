# background_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
import logging


class BackgroundWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        self.setGeometry(main_widget.rect())
        self.setFixedSize(main_widget.size())

    def paintEvent(self, event):
        logging.debug("BackgroundWidget.paintEvent called")
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.main_widget.background.paint_background(self, painter)
        painter.end()

    def resizeEvent(self, event):
        self.setGeometry(self.main_widget.rect())
        self.setFixedSize(self.main_widget.size())
