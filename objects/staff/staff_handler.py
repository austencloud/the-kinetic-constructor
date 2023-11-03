from PyQt6.QtCore import QObject
from objects.staff.staff_factory import StaffFactory
from objects.staff.staff_positioner import StaffPositioner
from objects.staff.staff_visibility_manager import StaffVisibilityManager
from objects.staff.staff_attributes import StaffAttributes
from objects.staff.staff_initializer import StaffInitializer

class StaffHandler(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.factory = StaffFactory(self)
        self.positioner = StaffPositioner(self)
        self.visibility_manager = StaffVisibilityManager(self)
        self.attributes = StaffAttributes(self)
        self.initializer = StaffInitializer(self.factory)