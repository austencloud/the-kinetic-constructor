from PyQt6.QtCore import QObject, QTimer, QPointF
from objects.arrow.arrow_manipulator import ArrowManipulator
from objects.arrow.arrow_positioner import ArrowPositioner
from objects.arrow.arrow_selector import ArrowSelector
from objects.arrow.arrow_factory import ArrowFactory
from objects.arrow.arrow_state_comparator import ArrowStateComparator
from objects.arrow.arrow_attributes import ArrowAttributes

class ArrowManager(QObject):
    def __init__(self, main_widget):
        super().__init__()
        self.remaining_staff = {}
        self.dragging_arrow = None
        self.drag_offset = QPointF(0, 0)
        self.timer = QTimer()
        self.letters = main_widget.letters
        self.main_widget = main_widget

        # Initialize the helper classes
        self.arrow_manipulator = ArrowManipulator(self)
        self.arrow_positioner = ArrowPositioner(self)
        self.arrow_selector = ArrowSelector(self)
        self.arrow_factory = ArrowFactory(self)
        self.arrow_state_comparator = ArrowStateComparator(self)
        self.arrow_attributes = ArrowAttributes(self)

