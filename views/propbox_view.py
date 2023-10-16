from PyQt5.QtWidgets import QGraphicsView, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from settings import *

class PropBox_View(QGraphicsView):
    def __init__(self, main_window, staff_manager, ui_setup):
        super().__init__()
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup

