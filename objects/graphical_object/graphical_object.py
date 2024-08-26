from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsItem
from data.constants import BLUE, RED


if TYPE_CHECKING:
    from widgets.base_widgets.pictograph.base_pictograph import BasePictograph

    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    svg_file: str = None
    self: Union["Arrow", "Prop"]
    ghost: Union["Arrow", "Prop"]
    is_ghost: bool = None
    color: str
    renderer: QSvgRenderer

    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

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
