from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent, QPainter
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetEvents:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def showEvent(self, event):
        super(self.main_widget.__class__, self.main_widget).showEvent(event)
        self.main_widget.background_handler.apply_background()
        self.main_widget.background_handler.setup_background()
        self.main_widget.ui_handler.load_current_tab()
        self.main_widget.background_widget.start_timer()


    def resizeEvent(self, event) -> None:
        super(self.main_widget.__class__, self.main_widget).resizeEvent(event)
        self.main_widget.navigation_widget.resize_navigation_widget()
