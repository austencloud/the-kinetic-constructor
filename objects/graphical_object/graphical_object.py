from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
import re
from typing import TYPE_CHECKING, Dict, Union


from constants import RED, BLUE, HEX_RED, HEX_BLUE
from objects.graphical_object.graphical_object_attr_manager import GraphicalObjectAttrManager
from objects.graphical_object.graphical_object_svg_manager import (
    GraphicalObjectSvgManager,
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
    is_ghost: bool
    color: Colors
    renderer: QSvgRenderer
    
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.svg_manager = GraphicalObjectSvgManager(self)
        self.attr_manager = GraphicalObjectAttrManager(self)
        # self.setup_graphics_flags()

    # ### SETUP ###

    # def setup_graphics_flags(self) -> None:
    #     self.setFlags(
    #         QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
    #         | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
    #         | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
    #     )
    #     self.setTransformOriginPoint(self.boundingRect().center())


    ### GETTERS ###

    def get_object_center(self) -> QPointF:
        if self.rotation() in [90, 270]:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
        elif self.rotation() in [0, 180]:
            return QPointF(
                (self.boundingRect().width() / 2), (self.boundingRect().height() / 2)
            )
