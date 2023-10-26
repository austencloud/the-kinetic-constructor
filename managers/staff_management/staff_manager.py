from PyQt6.QtCore import QObject
from managers.staff_management.staff_factory import StaffFactory
from managers.staff_management.staff_positioner import StaffPositioner

class StaffManager(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.staff_factory = StaffFactory(self)
        self.staff_positioner = StaffPositioner(self)
        
