from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsItem
from constants import BLUE, RED


from Enums.MotionAttributes import Color

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    svg_file: str = None
    self: Union["Arrow", "Prop"]
    ghost: Union["Arrow", "Prop"]
    is_ghost: bool = None
    color: Color
    renderer: QSvgRenderer

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def set_z_value_based_on_color(self) -> None:
        if self.color == RED:
            self.setZValue(5)  # Higher Z value for red props
        elif self.color == BLUE:
            self.setZValue(4)  # Lower Z value for blue props

    ### GETTERS ###

    def get_center(self) -> QPointF:
        if self.rotation() in [90, 270]:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
        elif self.rotation() in [0, 180]:
            return QPointF(
                (self.boundingRect().width() / 2), (self.boundingRect().height() / 2)
            )
        else:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
