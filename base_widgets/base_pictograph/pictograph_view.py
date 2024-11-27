import math
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPainter, QCursor, QKeyEvent, QMouseEvent

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

        # Basic setup without border logic
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        # Gestures and other initializations if necessary
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        self.setSceneRect(self.scene().itemsBoundingRect())
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def paintEvent(self, event):
        """Draw the pictograph."""
        super().paintEvent(event)
        # No border drawing here

    def enterEvent(self, event: QEvent) -> None:
        """Handle mouse entering the widget area."""
        # No border logic
        pass

    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leaving the widget area."""
        # No border logic
        pass

    # Additional methods and event handlers as needed
