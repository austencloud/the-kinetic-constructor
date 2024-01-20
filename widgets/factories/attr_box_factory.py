from typing import TYPE_CHECKING, List

from constants import (
    BLUE,
    COLOR,
    LEAD_STATE,
    LEADING,
    MOTION_TYPE,
    RED,
    TRAILING,
)

from widgets.attr_box.attr_box import AttrBox
from data.letter_engine_data import letter_type_motion_type_map

if TYPE_CHECKING:
    from widgets.attr_panel import AttrPanel


class AttrBoxFactory:
    def __init__(self, attr_panel: "AttrPanel") -> None:
        self.attr_panel = attr_panel

    def create_boxes(self) -> List[AttrBox]:
        attributes = []
        if (
            self.attr_panel.attribute_type == MOTION_TYPE
            and self.attr_panel.filter_tab.letter_type is not None
        ):
            attributes = letter_type_motion_type_map[
                self.attr_panel.filter_tab.letter_type
            ]
        elif self.attr_panel.attribute_type == COLOR:
            attributes = [BLUE, RED]
        elif self.attr_panel.attribute_type == LEAD_STATE:
            attributes = [LEADING, TRAILING]

        return [
            AttrBox(
                self.attr_panel,
                self.attr_panel.attribute_type,
                attribute,
            )
            for attribute in attributes
        ]
