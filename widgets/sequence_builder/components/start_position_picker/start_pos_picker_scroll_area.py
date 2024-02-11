from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from data.rules import get_next_letters
from widgets.scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)


from ....pictograph.pictograph import Pictograph
from widgets.scroll_area.base_scroll_area import BasePictographScrollArea

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_position_picker import (
        StartPosPicker,
    )


class StartPosPickerScrollArea(BasePictographScrollArea):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.sequence_builder = start_pos_picker.sequence_builder
        self.clickable_option_handler = self.sequence_builder.clickable_option_handler
        self.letters = self.sequence_builder.main_widget.letters
        self.pictograph_factory = ScrollAreaPictographFactory(self)

        self.pictographs = {}
        self.set_layout("HBox")
        self.COLUMN_COUNT = 5

    def _add_start_pos_to_layout(
        self, start_pos: Pictograph, is_start_pos: bool
    ) -> None:
        start_pos.view.mousePressEvent = (
            self.clickable_option_handler.get_click_handler(start_pos, is_start_pos)
        )
        self.layout.addWidget(start_pos.view)
        self.pictographs[start_pos.letter] = start_pos

    def resize_start_pos_picker_scroll_area(self) -> None:
        self.setMinimumHeight(self.start_pos_picker.height())
        self.setMinimumWidth(self.start_pos_picker.width())

    def replace_hbox_with_vbox(self):
        self.layout.removeItem(self.layout)
        self.set_layout("VBox")
