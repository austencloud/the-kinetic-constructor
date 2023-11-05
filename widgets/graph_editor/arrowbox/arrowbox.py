from PyQt6.QtWidgets import (
    QGraphicsView,
    QFrame,
    QGraphicsScene,
    QGraphicsItem,
    QGridLayout,
)
from settings.numerical_constants import GRAPHBOARD_SCALE, ARROWBOX_SCALE
from settings.string_constants import *
from PyQt6.QtCore import Qt
from objects.arrow.arrow import Arrow


class Arrowbox(QGraphicsScene):
    def __init__(self, main_widget, graphboard, infobox, arrow_manager):
        super().__init__()
        self.infobox = infobox
        self.drag_preview = None
        self.drag_state = {}
        self.dragging = False
        self.view = graphboard
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.arrow_manager = arrow_manager
        self.arrow_factory = self.arrow_manager.factory
        self.configure_arrowbox_frame()
        self.scale = ARROWBOX_SCALE
        self.populate_arrows()
        self.setSceneRect(0, 0, int(450), int(450))
        self.view = QGraphicsView(self)
        self.view.setAcceptDrops(True)
        self.view.setFrameShape(QFrame.Shape.NoFrame)
        self.view.setScene(self)
        self.objectbox_layout.addWidget(self.view)
        self.view.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.current_quadrant = None
        self.drag_manager = self.main_widget.drag_manager
        self.drag_preview = None
        self.view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)

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

        red_iso_arrow = self.arrow_factory.create_arrow(self.view, arrow1)
        blue_anti_arrow = self.arrow_factory.create_arrow(self.view, arrow2)

        arrows = [red_iso_arrow, blue_anti_arrow]

        for arrow in arrows:
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.main_widget.arrows.append(arrow)

        # set positions
        red_iso_arrow.setPos(100, 25)
        blue_anti_arrow.setPos(25, 25)

    def mousePressEvent(self, event):
        scenePos = event.scenePos()  # Directly get the scene position
        items = self.items(scenePos)
        arrows = [item for item in items if isinstance(item, Arrow)]
        if arrows:
            self.dragged_item = arrows[0]
        if arrows and event.button() == Qt.MouseButton.LeftButton:
            self.drag_manager.event_handler.start_drag(
                self.view, self.dragged_item, scenePos
            )
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        self.drag_manager.event_handler.handle_mouse_move(self.view, event)

    def mouseReleaseEvent(self, event):
        self.drag_manager.event_handler.handle_mouse_release(event)
