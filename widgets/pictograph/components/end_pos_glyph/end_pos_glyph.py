from typing import TYPE_CHECKING
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer
import os

from Enums.letters import LetterType
from path_helpers import get_images_and_data_path

if TYPE_CHECKING:

    from widgets.pictograph.pictograph import Pictograph

SVG_PATHS = {"alpha": "α.svg", "beta": "β.svg", "gamma": "Γ.svg"}
SVG_BASE_PATH = get_images_and_data_path("images/letters_trimmed/Type6")
SVG_PATHS = {
    letter_type: f"{SVG_BASE_PATH}/{path}" for letter_type, path in SVG_PATHS.items()
}


class EndPositionGlyph(QGraphicsSvgItem):

    def __init__(self, pictograph: "Pictograph"):
        super().__init__()  # Ensure the parent is set correctly
        self.pictograph = pictograph
        self.renderer: QSvgRenderer = QSvgRenderer()
        self.setSharedRenderer(self.renderer)
        self.setVisible(False)  # Initially invisible

    def update_position(self, end_pos):
        svg_file = os.path.join(SVG_BASE_PATH, SVG_PATHS.get(end_pos, ""))
        if self.renderer.load(svg_file):
            self.adjust_position()
            self.setVisible(True)  # Make visible only on successful load
            print(f"Loaded SVG file: {svg_file}")

        else:
            print(f"Failed to load SVG file: {svg_file}")

    def adjust_position(self):
        glyph_width = self.boundingRect().width()
        pictograph_width = self.pictograph.width()
        x_position = (pictograph_width - glyph_width) / 2
        y_position = 20  # Adjust y to a visible position within the pictograph bounds
        pos = QPointF(x_position, y_position)
        self.setPos(pos)
        print(f"Adjusted position to: {pos}")
        
    def addToScene(self):
        if not self.scene():
            self.pictograph.addItem(self)
