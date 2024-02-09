from typing import Union, TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker import StartPosPicker
    from widgets.sequence_builder.components.option_picker import OptionPicker
    from widgets.codex.codex import Codex
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class BasePictographScrollArea(QScrollArea):
    def __init__(
        self, parent: Union["StartPosPicker", "OptionPicker", "Codex"]
    ) -> None:
        super().__init__(parent)
        self.container = QWidget()
        self.main_widget = parent.main_widget
        self.container_layout = None
        self.setWidgetResizable(True)
        self.setup_ui()

    def setup_ui(self):
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_layout(self, layout_type: str):
        # Assign new layout based on type
        if layout_type == "VBox":
            new_layout = QVBoxLayout()
        elif layout_type == "HBox":
            new_layout = QHBoxLayout()
        else:
            raise ValueError("Invalid layout type specified.")

        self.container_layout = new_layout
        self.container.setLayout(self.container_layout)

    def clear_layout(self):
        # disattach the container from its layout
        if self.container_layout:
            while self.container_layout.count():
                child = self.container_layout.takeAt(0)
                if child.widget():
                    child.widget().hide()

            # del self.container_layout

    def add_widget_to_layout(self, widget: QWidget, section_index: int = None):
        if section_index >= 0:  # widget is a section
            self.container_layout.insertWidget(section_index, widget)
        else:  # widget is a start pos pictograph
            self.container_layout.addWidget(widget)
