from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from widgets.scroll_area.components.start_pos_picker_pictograph_factory import (
    StartPosPickerPictographFactory,
)
from widgets.sequence_builder.components.start_position_picker.choose_your_start_position_label import (
    ChooseYourStartPosLabel,
)
from widgets.sequence_builder.components.start_position_picker.start_pos_frame import (
    StartPosPickerPictographFrame,
)
from .start_pos_manager import StartPosManager
from .start_pos_picker_scroll_area import StartPosPickerScrollArea
from ....pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class StartPosPicker(QWidget):
    SPACING = 10

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.start_pos_cache: dict[str, Pictograph] = {}
        self.pictograph_factory = StartPosPickerPictographFactory(
            self, self.start_pos_cache
        )
        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.start_pos_manager = StartPosManager(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)

        self.pictograph_frame._setup_choose_your_start_pos_label()
        self.setup_layout()

    def setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        start_label_layout = QHBoxLayout()
        start_label_layout.addWidget(self.choose_your_start_pos_label)
        self.layout.addLayout(start_label_layout)

        pictograph_layout = QHBoxLayout()
        pictograph_layout.addWidget(self.pictograph_frame)
        self.layout.addLayout(pictograph_layout)

    def resize_start_position_picker(self) -> None:
        self.pictograph_frame.resize_start_pos_picker_pictograph_frame()
        self.start_pos_manager.resize_start_position_pictographs()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.choose_your_start_pos_label.show()

    def show_exciting_label(self):
        self.choose_your_start_pos_label.show()

    def hide_exciting_label(self):
        self.choose_your_start_pos_label.hide()
