from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
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
        self.start_options: dict[str, Pictograph] = {}
        self.scroll_area = StartPosPickerScrollArea(self)
        self.start_pos_manager = StartPosManager(self)
        self.setup_layout()

    def setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.scroll_area)

    def resize_start_position_picker(self) -> None:
        self.scroll_area.resize_start_pos_picker_scroll_area()
        self.start_pos_manager.resize_start_position_pictographs()