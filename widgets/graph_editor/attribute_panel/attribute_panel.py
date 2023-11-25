from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
)
from settings.string_constants import RED, BLUE
from widgets.graph_editor.attribute_panel.attribute_box import AttributeBox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard


class AttributePanel(QFrame):
    def __init__(self, graphboard: "GraphBoard") -> None:
        super().__init__()

        self.graphboard = graphboard

        self.setFixedHeight(self.graphboard.graph_editor.height())
        self.setFixedWidth(int(self.height() / 2))

        self.setContentsMargins(0, 0, 0, 0)

        self.blue_attr_box = AttributeBox(self, graphboard, BLUE)
        self.red_attr_box = AttributeBox(self, graphboard, RED)

        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self.blue_attr_box)
        self.layout().addWidget(self.red_attr_box)


    def update_attribute_panel(self) -> None:
        blue_arrow = self.graphboard.get_arrow_by_color(BLUE)
        red_arrow = self.graphboard.get_arrow_by_color(RED)

        if blue_arrow:
            self.blue_attr_box.update_labels(blue_arrow)
        if red_arrow:
            self.red_attr_box.update_labels(red_arrow)

    def update_attribute_panel_size(self) -> None:
        self.setFixedHeight(self.graphboard.view.height())
        self.setFixedWidth(int(self.height() / 2))
        self.blue_attr_box.update_attribute_box_size()
        self.red_attr_box.update_attribute_box_size()
        