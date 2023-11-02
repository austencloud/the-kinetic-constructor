from PyQt6.QtCore import QObject, QTimer, QPointF
from objects.arrow.arrow_manipulator import ArrowManipulator
from objects.arrow.arrow_positioner import ArrowPositioner
from objects.arrow.arrow_selector import ArrowSelector
from objects.arrow.arrow_factory import ArrowFactory
from objects.arrow.arrow_state_comparator import ArrowStateComparator
from objects.arrow.arrow_attributes import ArrowAttributes
from objects.arrow.arrow_drag_handler import ArrowDragHandler
class ArrowManager(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget

        # Initialize the helper classes
        self.manipulator = ArrowManipulator(self)
        self.positioner = ArrowPositioner(self)
        self.selector = ArrowSelector(self)
        self.attributes = ArrowAttributes(self)
        self.factory = ArrowFactory(self)
        self.state_comparator = ArrowStateComparator(self) 
        self.drag_handler = ArrowDragHandler(self)
        

