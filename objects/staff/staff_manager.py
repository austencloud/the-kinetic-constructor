from PyQt6.QtCore import QObject
from objects.staff.staff_factory import StaffFactory
from objects.staff.staff_positioner import StaffPositioner
from objects.staff.staff_manipulator import StaffManipulator
from objects.staff.staff_selector import StaffSelector
class StaffManager(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.staff_factory = StaffFactory(self)
        self.staff_positioner = StaffPositioner(self)
        self.staff_manipulator = StaffManipulator(self)
        self.staff_selector = StaffSelector(self)