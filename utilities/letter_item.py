from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from typing import TYPE_CHECKING

from widgets.letter import Letter

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class LetterItem(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.p = pictograph

    def position_letter_item(self) -> None:
        x = int(self.boundingRect().height() / 2)
        y = int(self.p.height() - (self.boundingRect().height() * 1.5))
        self.setPos(x, y)

    def set_letter_renderer(self) -> None:
        svg_path = f"images/letters_trimmed/{self.p.letter.type}/{self.p.letter.str}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.setSharedRenderer(renderer)

    def update_letter(self) -> None:
        if all(motion.motion_type for motion in self.p.motions.values()):
            self.p.letter = Letter(self.p.letter_calculator.get_current_letter())
            self.set_letter_renderer()
            self.position_letter_item()
        else:
            self.p.letter = None
            svg_path = f"images/letter_button_icons/blank.svg"
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.p.letter_item.setSharedRenderer(renderer)
