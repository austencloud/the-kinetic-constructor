import json
import os
from typing import TYPE_CHECKING, Union
from constants import BLUE, RED

from utilities.TypeChecking.prop_types import PropTypes
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.codex_scroll_area import CodexScrollArea
from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
    OptionPickerScrollArea,
)
from widgets.sequence_builder.components.start_position_picker.start_pos_picker_scroll_area import (
    StartPosPickerScrollArea,
)

if TYPE_CHECKING:
    from main_window import MainWindow




class PropTypeChanger:
    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window

    def replace_props(self, new_prop_type, pictograph: Pictograph):
        for color, prop in pictograph.props.items():
            new_prop = pictograph.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type
            )
            pictograph.props[color].deleteLater()
            pictograph.props[color].hide()
            pictograph.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.motions[color].prop = pictograph.props[color]
            pictograph.props[color].motion.attr_manager.update_prop_ori()
            pictograph.props[color].updater.update_prop()
        pictograph.red_prop = pictograph.props[RED]
        pictograph.blue_prop = pictograph.props[BLUE]
        pictograph.updater.update_pictograph()
