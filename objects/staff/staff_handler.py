from PyQt6.QtCore import QObject
from objects.staff.staff_factory import StaffFactory
from objects.staff.staff_positioner import StaffPositioner
from objects.staff.staff_selector import StaffSelector
from objects.staff.staff_attributes import StaffAttributes


class StaffHandler(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.factory = StaffFactory(self)
        self.positioner = StaffPositioner(self)
        self.selector = StaffSelector(self)
        self.attributes = StaffAttributes(self)
