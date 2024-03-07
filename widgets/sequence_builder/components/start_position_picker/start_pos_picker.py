from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from widgets.sequence_builder.components.start_position_picker.start_pos_pictograph_frame import StartPosPickerPictographFrame
from ....scroll_area.components.start_pos_picker_pictograph_factory import (
    StartPosPickerPictographFactory,
)
from ..start_position_picker.choose_your_next_pictograph_label import (
    ChooseYourStartPositionLabel,
)

from .start_pos_manager import StartPosManager
from ....pictograph.pictograph import Pictograph
from .start_pos_variation_dialog import StartPosVariationDialog

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
        self.choose_your_start_pos_label = ChooseYourStartPositionLabel(self)
        self.variation_dialog = StartPosVariationDialog(self)

        self.setup_layout()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        start_label_layout = QHBoxLayout()
        pictograph_layout = QHBoxLayout()

        start_label_layout.addWidget(self.choose_your_start_pos_label)
        pictograph_layout.addWidget(self.pictograph_frame)

        self.layout.addLayout(start_label_layout, 1)
        self.layout.addLayout(pictograph_layout, 4)

    def resize_start_position_picker(self) -> None:
        self.pictograph_frame.resize_start_pos_picker_pictograph_frame()
        self.start_pos_manager.resize_start_position_pictographs()
        
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.choose_your_start_pos_label.show()

    def show_variation_dialog(self, position: str) -> None:
        self.variation_dialog.load_variations(position)
        if self.variation_dialog.exec():
            selected_variation = self.variation_dialog.get_selected_variation()
            self.start_pos_manager.on_start_pos_clicked(selected_variation)