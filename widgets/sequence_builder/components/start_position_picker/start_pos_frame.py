from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosPickerPictographFrame(QWidget):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.clickable_option_handler = (
            self.start_pos_picker.sequence_builder.option_click_handler
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictographs_layout = QHBoxLayout()
        self.layout.addLayout(self.pictographs_layout)

    def _setup_choose_your_start_pos_label(self):
        self.label = self.start_pos_picker.choose_your_start_pos_label
        self.layout.addWidget(self.label)

    def resize_start_pos_picker_pictograph_frame(self) -> None:
        self.setMinimumHeight(self.start_pos_picker.height())
        self.setMinimumWidth(self.start_pos_picker.width())
        self.start_pos_picker.choose_your_start_pos_label.set_stylesheet()

    def _add_start_pos_to_layout(self, start_pos: Pictograph) -> None:
        start_pos.view.mousePressEvent = (
            self.clickable_option_handler.get_click_handler(start_pos)
        )
        self.pictographs_layout.addWidget(start_pos.view)
        self.start_pos_picker.start_pos_cache[start_pos.letter] = start_pos
        key = f"{start_pos.letter}_{start_pos.start_pos}_{start_pos.end_pos}"
        self.start_pos_picker.main_widget.all_pictographs[start_pos.letter][
            key
        ] = start_pos
