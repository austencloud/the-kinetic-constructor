from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsItem


from objects.graphical_object.svg_manager import (
    SvgManager,
)
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    svg_file: str
    self: Union["Arrow", "Prop"]
    ghost: Union["Arrow", "Prop"]
    is_ghost: bool = None
    color: Colors
    renderer: QSvgRenderer

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.svg_manager = SvgManager(self)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True
        )  
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
