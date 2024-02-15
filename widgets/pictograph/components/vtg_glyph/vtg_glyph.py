from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING

from Enums.Enums import LetterType, VTG_Modes
from constants import SpecificPositions as SP


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph

SVG_PATHS = {
    VTG_Modes.SPLIT_SAME: "SS.svg",
    VTG_Modes.SPLIT_OPP: "SO.svg",
    VTG_Modes.TOG_SAME: "TS.svg",
    VTG_Modes.TOG_OPP: "TO.svg",
    VTG_Modes.QUARTER_SAME: "QS.svg",
    VTG_Modes.QUARTER_OPP: "QO.svg",
}

SVG_BASE_PATH = "images/vtg_glyphs"
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class VTG_Glyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def set_vtg_mode(self):
        if not self.pictograph.letter_type in [LetterType.Type1]:
            return
        vtg_mode = self.determine_vtg_mode()
        self.pictograph.vtg_mode = vtg_mode
        svg_path: str = SVG_PATHS.get(vtg_mode, "")
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            self.pictograph.addItem(self)
            self.position_vtg_glyph()
            visibility_manager = (
                self.pictograph.main_widget.main_window.settings_manager.glyph_visibility_manager
            )
            self.setVisible(visibility_manager.should_glyph_be_visible("VTG"))

        print(f"SVG path: {svg_path}")  # Add this line for debug output

    def determine_vtg_mode(self):
        letter = self.pictograph.letter
        mode = self.pictograph.vtg_mode
        start_pos = self.pictograph.start_pos

        if letter in ["A", "B", "C"]:
            mode = VTG_Modes.SPLIT_SAME
        elif letter in ["D", "E", "F"]:
            if start_pos in [SP.BETA2.value, SP.BETA4.value]:
                mode = VTG_Modes.SPLIT_OPP
            elif start_pos in [SP.BETA1.value, SP.BETA3.value]:
                mode = VTG_Modes.TOG_OPP
        elif letter in ["G", "H", "I"]:
            mode = VTG_Modes.TOG_SAME
        elif letter in ["J", "K", "L"]:
            if start_pos in [SP.ALPHA1.value, SP.ALPHA3.value]:
                mode = VTG_Modes.SPLIT_OPP
            elif start_pos in [SP.ALPHA2.value, SP.ALPHA4.value]:
                mode = VTG_Modes.TOG_OPP
        elif letter in ["M", "N", "O", "P", "Q", "R"]:
            mode = VTG_Modes.QUARTER_OPP
        elif letter in ["S", "T", "U", "V"]:
            mode = VTG_Modes.QUARTER_SAME

        return mode

    def position_vtg_glyph(self) -> None:
        pictograph_width = self.pictograph.width()
        pictograph_height = self.pictograph.height()

        scale_factor = 0.7
        self.setScale(scale_factor)

        border_percentage = 0.03
        additional_margin_percentage = 0.03

        border_offset_width = pictograph_width * border_percentage
        border_offset_height = pictograph_height * border_percentage
        additional_margin_width = pictograph_width * additional_margin_percentage
        additional_margin_height = pictograph_height * additional_margin_percentage

        effective_pictograph_width = pictograph_width - 2 * (
            border_offset_width + additional_margin_width
        )
        effective_pictograph_height = pictograph_height - 2 * (
            border_offset_height + additional_margin_height
        )

        scaled_width = self.boundingRect().width() * scale_factor
        scaled_height = self.boundingRect().height() * scale_factor

        x = (
            effective_pictograph_width
            - scaled_width
            + (border_offset_width + additional_margin_width)
        )
        y = (
            effective_pictograph_height
            - scaled_height
            + (border_offset_height + additional_margin_height)
        )

        self.setPos(x, y)
        self.setTransformOriginPoint(scaled_width / 2, scaled_height / 2)

        print(f"VTG_Glyph positioned with additional inner margin: {x}, {y}")
