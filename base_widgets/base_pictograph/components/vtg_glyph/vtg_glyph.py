from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING, Literal

from Enums.Enums import LetterType
from data.constants import (
    ALPHA1,
    alpha3,
    alpha5,
    alpha7,
    BETA1,
    beta3,
    beta5,
    beta7,
    QUARTER_OPP,
    QUARTER_SAME,
    SPLIT_OPP,
    SPLIT_SAME,
    TOG_OPP,
    TOG_SAME,
)
from utilities.path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


SVG_PATHS = {
    SPLIT_SAME: "SS.svg",
    SPLIT_OPP: "SO.svg",
    TOG_SAME: "TS.svg",
    TOG_OPP: "TO.svg",
    QUARTER_SAME: "QS.svg",
    QUARTER_OPP: "QO.svg",
}

SVG_BASE_PATH = get_images_and_data_path("images/vtg_glyphs")
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class VTG_Glyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def set_vtg_mode(self) -> None:
        if not self.pictograph.letter_type in [LetterType.Type1]:
            return
        vtg_mode = self.determine_vtg_mode()
        self.pictograph.vtg_mode = vtg_mode
        svg_path: str = SVG_PATHS.get(vtg_mode, "")
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            # if self isn't already in self.pictograph, then add it
            if not self.scene():
                self.pictograph.addItem(self)
            self.position_vtg_glyph()
            visibility_manager = (
                self.pictograph.main_widget.main_window.settings_manager.visibility.glyph_visibility_manager
            )
            self.setVisible(visibility_manager.should_glyph_be_visible("VTG"))

    def determine_vtg_mode(self) -> Literal["SS", "SO", "TS", "TO", "QS", "QO"]:
        letter_str = self.pictograph.letter.value
        mode = self.pictograph.vtg_mode
        start_pos = self.pictograph.start_pos

        if letter_str in ["A", "B", "C"]:
            mode = SPLIT_SAME
        elif letter_str in ["D", "E", "F"]:
            if start_pos in [beta3, beta7]:
                mode = SPLIT_OPP
            elif start_pos in [BETA1, beta5]:
                mode = TOG_OPP
        elif letter_str in ["G", "H", "I"]:
            mode = TOG_SAME
        elif letter_str in ["J", "K", "L"]:
            if start_pos in [ALPHA1, alpha5]:
                mode = SPLIT_OPP
            elif start_pos in [alpha3, alpha7]:
                mode = TOG_OPP
        elif letter_str in ["M", "N", "O", "P", "Q", "R"]:
            mode = QUARTER_OPP
        elif letter_str in ["S", "T", "U", "V"]:
            mode = QUARTER_SAME

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
