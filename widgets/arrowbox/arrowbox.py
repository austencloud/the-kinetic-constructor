from PyQt6.QtWidgets import (
    QGraphicsView,
    QFrame,
    QGraphicsScene,
    QGraphicsItem,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QPointF
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import (
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    PRO,
    CLOCKWISE,
    NORTHEAST,
    ANTI,
    COUNTER_CLOCKWISE,
    RED,
    BLUE,
    NORTH,
    EAST,
)
from objects.arrow import Arrow
from widgets.arrowbox.arrowbox_drag import ArrowBoxDrag
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.infobox.infobox import InfoBox
    from objects.arrow import Arrow

from utilities.TypeChecking.TypeChecking import ArrowAttributesDicts

class ArrowBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", infobox: "InfoBox") -> None:
        super().__init__()
        self.infobox = infobox
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.setup_frame()
        self.setup_view()
        self.populate_arrows()
        self.setSceneRect(0, 0, 450, 450)
        self.arrowbox_layout.addWidget(self.view)
        self.arrowbox_drag = None

    def setup_view(self) -> None:
        view = QGraphicsView(self)
        view.setAcceptDrops(True)
        view.setFrameShape(QFrame.Shape.NoFrame)
        view.setScene(self)
        view.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        self.view = view

    def setup_frame(self) -> None:
        self.arrowbox_frame = QFrame(self.main_widget.main_window)
        self.arrowbox_layout = QGridLayout()
        self.arrowbox_frame.setLayout(self.arrowbox_layout)

    def populate_arrows(self) -> None:
        self.arrows: List[Arrow] = []
        initial_arrow_attribute_collection: List[ArrowAttributesDicts] = [
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

        for dict in initial_arrow_attribute_collection:
            arrow = Arrow(self, dict)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.arrows.append(arrow)

        self.arrows[0].setPos(150, 25)
        self.arrows[1].setPos(25, 25)

    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        if self.items(QPointF(scene_pos)):
            if not self.arrowbox_drag:
                graphboard = self.main_widget.graphboard
                self.arrowbox_drag = ArrowBoxDrag(self.main_window, graphboard, self)

            arrows = [
                item
                for item in self.items(QPointF(scene_pos))
                if isinstance(item, Arrow)
            ]

            if arrows:
                self.target_arrow = arrows[0]
                if event.button() == Qt.MouseButton.LeftButton:
                    self.arrowbox_drag.match_target_arrow(self.target_arrow)
                    self.arrowbox_drag.start_drag(event_pos)
            else:
                event.ignore()

    def mouseMoveEvent(self, event) -> None:
        if self.arrowbox_drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.arrowbox_drag.handle_mouse_move(event_pos)

    def mouseReleaseEvent(self, event) -> None:
        if self.arrowbox_drag:
            self.arrowbox_drag.handle_mouse_release()
