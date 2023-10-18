from PyQt6.QtWidgets import QGraphicsView, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from settings import *

class PropBox_View(QGraphicsView):
    def __init__(self, main_window, staff_manager, main_widget):
        super().__init__()
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.main_widget = main_widget

