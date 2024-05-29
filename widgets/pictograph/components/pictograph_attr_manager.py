from typing import TYPE_CHECKING

from Enums.Enums import Letter
from data.constants import LETTER


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographAttrManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def update_attributes(self, pictograph_dict: dict) -> None:
        for attr_name, attr_value in pictograph_dict.items():
            if attr_name == LETTER:
                attr_value = Letter.get_letter(attr_value)
            if attr_value is not None:
                setattr(self.pictograph, attr_name, attr_value)
