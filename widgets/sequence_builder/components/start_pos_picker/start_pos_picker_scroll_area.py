from typing import TYPE_CHECKING

from widgets.sequence_builder.option_picker.option_picker_pictograph_factory import OptionPickerPictographFactory




from ....pictograph.pictograph import Pictograph
from widgets.base_widgets.base_picker_scroll_area import BasePickerScrollArea

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )


class StartPosPickerScrollArea(BasePickerScrollArea):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.sequence_builder = start_pos_picker.sequence_builder
        self.clickable_option_handler = self.sequence_builder.option_click_handler
        self.letters = self.sequence_builder.top_builder_widget.letters
        self.pictograph_cache: dict[str, Pictograph] = {}
        self.pictograph_factory = OptionPickerPictographFactory(
            self, self.pictograph_cache
        )
        self.set_layout("HBox")
        self.COLUMN_COUNT = 5

    def _add_start_pos_to_layout(self, start_pos: Pictograph) -> None:
        start_pos.view.mousePressEvent = (
            self.clickable_option_handler.get_click_handler(start_pos)
        )
        self.layout.addWidget(start_pos.view)
        self.pictograph_cache[start_pos.letter] = start_pos
        key = f"{start_pos.letter}_{start_pos.start_pos}_{start_pos.end_pos}"
        self.main_widget.pictograph_cache[start_pos.letter][key] = start_pos

    def resize_start_pos_picker_scroll_area(self) -> None:
        self.setMinimumHeight(self.start_pos_picker.height())
        self.setMinimumWidth(self.start_pos_picker.width())

    def replace_hbox_with_vbox(self):
        self.layout.removeItem(self.layout)
        self.set_layout("VBox")
