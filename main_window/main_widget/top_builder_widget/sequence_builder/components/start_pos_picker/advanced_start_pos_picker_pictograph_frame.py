from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from typing import TYPE_CHECKING
from widgets.base_widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from ...advanced_start_pos_picker.advanced_start_pos_picker import AdvancedStartPosPicker


class AdvancedStartPosPickerPictographFrame(QWidget):
    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker"):
        super().__init__(advanced_start_pos_picker)
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.clickable_option_handler = (
            self.advanced_start_pos_picker.sequence_builder.option_click_handler
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictographs_layout = QHBoxLayout()
        self.layout.addLayout(self.pictographs_layout)
        self.variation_buttons: dict[str, QPushButton] = {}
        self.start_positions: dict[str, Pictograph] = {}

    def _add_start_pos_to_layout(self, start_pos: Pictograph) -> None:
        start_pos.view.mousePressEvent = (
            self.clickable_option_handler.get_click_handler(start_pos)
        )
        self.pictographs_layout.setSpacing(5)  # Adjust spacing between pictographs
        self.pictographs_layout.addWidget(start_pos.view)
        self.advanced_start_pos_picker.start_pos_cache[start_pos.letter] = start_pos
        key = f"{start_pos.letter}_{start_pos.start_pos}_{start_pos.end_pos}"
        self.advanced_start_pos_picker.main_widget.pictograph_cache[start_pos.letter][
            key
        ] = start_pos
        self.start_positions[start_pos.letter] = start_pos
