from PyQt6.QtWidgets import QHBoxLayout, QFrame
from typing import TYPE_CHECKING
from widgets.factories.attr_box_factory import AttrBoxFactory
if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab

class AttrPanel(QFrame):
    def __init__(self, filter_tab: "FilterTab", attribute_type) -> None:
        super().__init__()
        self.filter_tab = filter_tab
        self.attribute_type = attribute_type
        self.attr_box_factory = AttrBoxFactory(self)
        self.boxes = self.attr_box_factory.create_boxes()
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for box in self.boxes:
            self.layout.addWidget(box)

    def resize_attr_panel(self) -> None:
        for box in self.boxes:
            box.resize_attr_box()
