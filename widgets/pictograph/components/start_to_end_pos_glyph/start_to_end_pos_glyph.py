from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
import os

from path_helpers import get_images_and_data_path  # Assuming correct import

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class StartToEndPosGlyph(QGraphicsItemGroup):
    def __init__(self, pictograph: "Pictograph"):
        super().__init__()
        self.pictograph = pictograph
        self.glyph_visibility_manager = (
            self.pictograph.main_widget.main_window.settings_manager.glyph_visibility_manager
        )

        # Initialize SVG items
        self.start_glyph = QGraphicsSvgItem(self)
        self.arrow_glyph = QGraphicsSvgItem(self)
        self.end_glyph = QGraphicsSvgItem(self)

        # Load SVG renderers
        self.renderer_start = QSvgRenderer()
        self.renderer_arrow = QSvgRenderer()
        self.renderer_end = QSvgRenderer()

        # Set paths
        self.SVG_BASE_PATH = get_images_and_data_path("images/letters_trimmed/Type6")
        self.SVG_ARROW_PATH = get_images_and_data_path("images/arrow.svg")
        self.SVG_PATHS = {"alpha": "α.svg", "beta": "β.svg", "gamma": "Γ.svg"}

    def set_start_to_end_pos_glyph(self):
        start_pos = self.pictograph.start_pos[
            :-1
        ]  # Assuming start_pos ends with a numeral
        end_pos = self.pictograph.end_pos[:-1]  # Assuming end_pos ends with a numeral

        # Construct full paths for SVG files
        svg_file_start = os.path.join(
            self.SVG_BASE_PATH, self.SVG_PATHS.get(start_pos, "")
        )
        svg_file_end = os.path.join(self.SVG_BASE_PATH, self.SVG_PATHS.get(end_pos, ""))
        svg_file_arrow = self.SVG_ARROW_PATH

        # Load SVG content into the renderers
        if (
            self.renderer_start.load(svg_file_start)
            and self.renderer_arrow.load(svg_file_arrow)
            and self.renderer_end.load(svg_file_end)
        ):

            # Set the renderer for each SVG item
            self.start_glyph.setSharedRenderer(self.renderer_start)
            self.arrow_glyph.setSharedRenderer(self.renderer_arrow)
            self.end_glyph.setSharedRenderer(self.renderer_end)

            self.scale_and_position_glyphs()

            # Adjust visibility based on settings
            visible = self.glyph_visibility_manager.should_glyph_be_visible(
                "EndPosition"
            )
            self.setVisible(visible)
        else:
            print(
                f"Failed to load SVG files: {svg_file_start}, {svg_file_arrow}, {svg_file_end}"
            )

    def scale_and_position_glyphs(self):
        # Apply a uniform scaling
        scale_factor = 0.75
        self.start_glyph.setScale(scale_factor)
        self.arrow_glyph.setScale(scale_factor)
        self.end_glyph.setScale(scale_factor)

        # Position glyphs horizontally
        spacing = 25  # Adjust the spacing value as desired
        self.start_glyph.setPos(0, 0)

        self.end_glyph.setPos(
            self.start_glyph.boundingRect().width() * scale_factor
            + self.arrow_glyph.boundingRect().width() * scale_factor
            + spacing,  # Increase the spacing between glyphs
            0,
        )

        # Update the y-position of the arrow glyph to be vertically centered

        # Update group position to center on the pictograph
        total_width = (
            self.start_glyph.boundingRect().width() * scale_factor
            + self.arrow_glyph.boundingRect().width() * scale_factor
            + self.end_glyph.boundingRect().width() * scale_factor
            + spacing  # Increase the spacing between glyphs
        )
        x_position = (self.pictograph.width()) // 2 - (total_width // 2)
        y_position = 50

        # Adjust the y-position of the arrow glyph to match the vertical center of the letters
        self.arrow_glyph.setPos(
            self.start_glyph.boundingRect().width() * scale_factor
            + spacing * scale_factor,
            self.start_glyph.boundingRect().height() * scale_factor // 2
            - self.arrow_glyph.boundingRect().height() * scale_factor,
        )
        self.setPos(x_position, y_position)

    def addToScene(self):
        if not self.scene():
            self.pictograph.addItem(self)
            print(f"Start to end position glyphs added to scene.")
