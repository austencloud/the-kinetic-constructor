from typing import Union, TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.build_tab.option_picker.option_picker import (
        OptionPicker,
    )
    from main_window.main_widget.build_tab.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )


class BasePickerScrollArea(QScrollArea):
    def __init__(self, parent: Union["StartPosPicker", "OptionPicker"]) -> None:
        super().__init__(parent)
        self.container = QWidget()
        self.main_widget = parent.main_widget
        self.layout: Union[QVBoxLayout, QHBoxLayout] = None
        self.setWidgetResizable(True)
        self.setup_ui()

    def setup_ui(self):
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_layout(self, layout_type: str):
        if layout_type == "VBox":
            new_layout = QVBoxLayout()
        elif layout_type == "HBox":
            new_layout = QHBoxLayout()
        else:
            raise ValueError("Invalid layout type specified.")

        self.layout = new_layout
        self.container.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
