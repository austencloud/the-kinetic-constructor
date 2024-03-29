from typing import Union, TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from Enums.letters import LetterType


if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )
    from widgets.sequence_builder.components.option_picker.option_picker import (
        OptionPicker,
    )
    from widgets.letterbook.letterbook import LetterBook


class BasePictographScrollArea(QScrollArea):
    def __init__(
        self, parent: Union["StartPosPicker", "OptionPicker", "LetterBook"]
    ) -> None:
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
        # setup group widget section at the bottom

    def add_section_to_layout(self, section: QWidget, section_index: int = None):
        if section_index == 0 or section_index:  # widget is a section
            if section.__class__.__name__ == "OptionPickerSectionWidget":
                if section.letter_type == LetterType.Type1:
                    self.layout.insertWidget(section_index, section, 6)
                else:
                    self.layout.insertWidget(section_index, section, 4)
            elif section.__class__.__name__ == "SectionGroupWidget":
                self.layout.insertWidget(
                    section_index, section, 4
                )  # Set stretch factor to 4 for group widgets
