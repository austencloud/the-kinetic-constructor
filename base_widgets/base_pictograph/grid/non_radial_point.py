from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import QPointF, Qt

if TYPE_CHECKING:
    from .non_radial_points_toggler import NonRadialPointsToggler


class NonRadialGridPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, r, point_id, visibility_manager: "NonRadialPointsToggler"):
        super().__init__(-r, -r, 2 * r, 2 * r)
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setPos(QPointF(x, y))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.setToolTip(point_id)
        self.point_id = point_id
        self.visibility_manager = visibility_manager
        self.setZValue(101)
