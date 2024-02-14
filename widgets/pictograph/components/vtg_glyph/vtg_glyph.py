from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING

from Enums.Enums import LetterType, VTG_Modes
from constants import SpecificPositions as SP


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


# SVG_PATHS = {
#     pass: "pass.svg",
# }

# SVG_BASE_PATH = "images/letters_trimmed"
# SVG_PATHS = {
#     letter_type: f"{SVG_BASE_PATH}/{path}" for letter_type, path in SVG_PATHS.items()
# }


class VTG_Glyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.renderer = None

    def set_vtg_mode(self):
        if not self.pictograph.letter_type in [LetterType.Type1]:
            return
        if self.pictograph.letter in ["A", "B", "C"]:
            self.pictograph.vtg_mode = VTG_Modes.SPLIT_SAME.value
        elif self.pictograph.letter in ["D", "E", "F"]:
            if self.pictograph.start_pos in [SP.BETA2.value, SP.BETA4.value]:
                self.pictograph.vtg_mode = VTG_Modes.SPLIT_OPP.value
            elif self.pictograph.start_pos in [SP.BETA1.value, SP.BETA3.value]:
                self.pictograph.vtg_mode = VTG_Modes.TOG_OPP.value
        elif self.pictograph.letter in ["G", "H", "I"]:
            self.pictograph.vtg_mode = VTG_Modes.TOG_SAME.value
        elif self.pictograph.letter in ["J", "K", "L"]:
            if self.pictograph.start_pos in [SP.ALPHA1.value, SP.ALPHA3.value]:
                self.pictograph.vtg_mode = VTG_Modes.SPLIT_OPP.value
            elif self.pictograph.start_pos in [SP.ALPHA2.value, SP.ALPHA4.value]:
                self.pictograph.vtg_mode = VTG_Modes.TOG_OPP.value
        elif self.pictograph.letter in ["M", "N", "O", "P", "Q", "R"]:
            self.pictograph.vtg_mode = VTG_Modes.QUARTER_TIME_OPP.value
        elif self.pictograph.letter in ["S", "T", "U", "V"]:
            self.pictograph.vtg_mode = VTG_Modes.QUARTER_TIME_SAME.value

        self.vtg_mode = self.pictograph.vtg_mode
        letter_type = LetterType.get_letter_type(self.pictograph.letter)
        self.pictograph.letter_type = letter_type

    def position_letter(self) -> None:
        x = int(self.boundingRect().height() / 1.5)
        y = int(self.pictograph.height() - (self.boundingRect().height() * 1.7))
        self.setPos(x, y)
