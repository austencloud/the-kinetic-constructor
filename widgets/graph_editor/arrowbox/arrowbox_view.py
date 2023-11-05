import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QGraphicsView,
    QFrame,
    QGraphicsScene,
    QGraphicsItem,
    QFrame,
    QGridLayout,
)
from settings.numerical_constants import GRAPHBOARD_SCALE, ARROWBOX_SCALE
from settings.string_constants import *
from events.drag.drag_manager import DragManager
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from objects.arrow.arrow import Arrow


class ArrowBoxView(QGraphicsView):
    def __init__(self, main_widget, graphboard_view, infobox, arrow_manager):
        super().__init__()
        self.infobox = infobox
        self.drag_preview = None
        self.drag_state = {}
        self.dragging = False
        self.graphboard_view = graphboard_view
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.arrowbox_scene = QGraphicsScene()
        self.setScene(self.arrowbox_scene)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.arrow_manager = arrow_manager
        self.arrow_factory = self.arrow_manager.factory
        self.configure_arrowbox_frame()
        self.view_scale = ARROWBOX_SCALE
        self.populate_arrows()
        self.objectbox_layout.addWidget(self)
        self.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.current_quadrant = None
        self.drag_manager = self.main_widget.drag_manager
        self.drag_preview = None

    def configure_arrowbox_frame(self):
        self.arrowbox_frame = QFrame(self.main_window)
        self.objectbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.objectbox_layout)

    def populate_arrows(self):
        arrow1 = {
            COLOR: RED,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            QUADRANT: "ne",
            START_LOCATION: NORTH,
            END_LOCATION: EAST,
            TURNS: 0,
        }

        arrow2 = {
            COLOR: BLUE,
            MOTION_TYPE: ANTI,
            ROTATION_DIRECTION: COUNTER_CLOCKWISE,
            QUADRANT: "ne",
            START_LOCATION: NORTH,
            END_LOCATION: EAST,
            TURNS: 0,
        }

        red_iso_arrow = self.arrow_factory.create_arrow(self, arrow1)
        blue_anti_arrow = self.arrow_factory.create_arrow(self, arrow2)

        arrows = [red_iso_arrow, blue_anti_arrow]

        for arrow in arrows:
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.arrowbox_scene.addItem(arrow)
            self.main_widget.arrows.append(arrow)

        # set positions
        red_iso_arrow.setPos(100, 50)
        blue_anti_arrow.setPos(50, 50)

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        items = self.scene().items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            self.dragged_item = arrows[0]
        if arrows and event.button() == Qt.MouseButton.LeftButton:
            self.drag_manager.event_handler.start_drag(self, self.dragged_item, event)

            # if the user clicked on an item and not the iew itself, then set self.dragging to true
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        self.drag_manager.event_handler.handle_mouse_move(self, event)

    def mouseReleaseEvent(self, event):
        self.drag_manager.event_handler.handle_mouse_release(event)
