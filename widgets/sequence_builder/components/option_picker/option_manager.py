from PyQt6.QtCore import QObject, pyqtSignal
from constants import END_POS, START_POS
from typing import TYPE_CHECKING

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker import (
        OptionPicker,
    )


class OptionManager(QObject):
    option_selected = pyqtSignal(Pictograph)

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__()
        self.sequence_builder = option_picker.sequence_builder
        self.main_widget = option_picker.main_widget
        self.start_options: dict[str, Pictograph] = {}

    def get_next_options(self, sequence) -> list[dict]:
        next_options = []

        last_pictograph_dict = sequence[-1]
        start_pos = last_pictograph_dict[END_POS]

        if start_pos:
            for dict_list in self.main_widget.letters.values():
                for dict in dict_list:
                    if dict[START_POS] == start_pos:
                        next_options.append(dict)

        return next_options
