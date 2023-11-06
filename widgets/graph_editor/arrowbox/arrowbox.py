from PyQt6.QtWidgets import (
    QGraphicsView,
    QFrame,
    QGraphicsScene,
    QGraphicsItem,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *
from objects.arrow.arrow import Arrow


class Arrowbox(QGraphicsScene):
    def __init__(self, main_widget, infobox):
        super().__init__()
        self.infobox = infobox
        self.main_widget = main_widget

        self.configure_frame()
        self.setup_view()
        self.populate_arrows()
        self.setSceneRect(0, 0, 450, 450)
        self.arrowbox_layout.addWidget(self.view)

        self.drag_manager = self.main_widget.drag_manager
        self.drag_preview = None
        

    def setup_view(self):
        self.view = QGraphicsView(self)
        self.view.setAcceptDrops(True)
        self.view.setFrameShape(QFrame.Shape.NoFrame)
        self.view.setScene(self)
        self.view.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)

    def configure_frame(self):
        self.arrowbox_frame = QFrame(self.main_widget.main_window)
        self.arrowbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.arrowbox_layout)

    def populate_arrows(self):
        self.arrows = []
        arrow_dicts = [
            {
                COLOR: RED,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                QUADRANT: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                QUADRANT: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
        ]

        for dict in arrow_dicts:
            arrow = Arrow(self, dict)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.arrows.append(arrow)

        # set positions
        self.arrows[0].setPos(150, 25)
        self.arrows[1].setPos(25, 25)

    def mousePressEvent(self, event):
        scene_pos = event.scenePos()
        view_pos = self.view.mapFromScene(scene_pos)
        arrows = [item for item in self.items(QPointF(scene_pos)) if isinstance(item, Arrow)]

        if arrows:
            self.dragged_item = arrows[0]
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_manager.event_handler.start_drag(
                    self, self.dragged_item, view_pos
                )
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        scene_pos = event.scenePos()
        view_pos = self.view.mapFromScene(scene_pos)
        self.drag_manager.event_handler.handle_mouse_move(self, event, view_pos)

    def mouseReleaseEvent(self, event):
        scene_pos = event.scenePos()
        view_pos = self.view.mapFromScene(scene_pos)
        self.drag_manager.event_handler.handle_mouse_release(event, view_pos)
