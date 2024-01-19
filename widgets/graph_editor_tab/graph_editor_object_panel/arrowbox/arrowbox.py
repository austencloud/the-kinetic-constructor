from typing import TYPE_CHECKING, Dict, List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QGridLayout,
    QComboBox,
    QLabel,
)
from objects.arrow.arrow import Arrow
from constants import *
from objects.arrow.ghost_arrow import GhostArrow
from objects.motion.motion import Motion
from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox_drag import (
    ArrowBoxDrag,
)
from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox_view import (
    ArrowBoxView,
)
from objects.grid import Grid
from PyQt6.QtCore import QPointF

from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox import (
    BaseObjectBox,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class ArrowBox(BaseObjectBox):
    def __init__(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__(main_widget, graph_editor)
        self.main_widget = main_widget
        self.view = ArrowBoxView(self, graph_editor)
        self.grid = Grid(self)
        self.target_arrow: "Arrow" = None
        self.drag = None
        self.default_start_ori = IN
        self.start_ori = self.default_start_ori

        self.arrowbox_layout = QGridLayout()
        self.arrowbox_layout.addWidget(self.view)

        # Adding the combo box for turns
        self.turns_combobox = QComboBox()
        self.turns_combobox.addItems(
            [str(i) for i in range(10)]
        )  # Assuming up to 9 turns
        self.turns_combobox.setCurrentIndex(0)  # Default to 0 turns
        self.turns_combobox.currentTextChanged.connect(self.on_turns_changed)

        self.arrowbox_layout.addWidget(
            QLabel("Turns:"), 0, 0
        )  # Label for the combo box
        self.arrowbox_layout.addWidget(
            self.turns_combobox, 0, 1
        )  # Adding the combo box to the layout

        self.motions: List[Motion] = self.create_motions()
        self.arrows: List[Arrow] = self.create_arrows()

    def on_turns_changed(self, turns: str) -> None:
        """Update turns for all arrows when the selected value in the combo box changes."""
        for arrow in self.arrows:
            arrow.turns = int(turns)
            arrow.update_arrow()  # Update the appearance of the arrow based on the new turns

    def create_arrows(self) -> None:
        red_arrows: List[Arrow] = []
        blue_arrows: List[Arrow] = []
        arrows: List[Arrow] = []
        for motion in self.motions:
            arrow_dict = {
                COLOR: motion.color,
                MOTION_TYPE: motion.motion_type,
                TURNS: int(self.turns_combobox.currentText()),
            }

            arrow = Arrow(self, arrow_dict, motion)
            arrow.ghost = GhostArrow(self, arrow_dict, motion)
            arrow.motion = motion
            arrow.ghost.motion = motion
            motion.arrow = arrow
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            arrows.append(arrow)

            if arrow.color == RED:
                red_arrows.append(arrow)
            elif arrow.color == BLUE:
                blue_arrows.append(arrow)
            arrow.setTransformOriginPoint(arrow.boundingRect().center())
            arrow.toggle_dimmer(True)

        red_arrow_positions: List[Tuple[int, int]] = [
            (525, 150),
            (525, 525),
            (475, 475),
            (475, 200),
        ]
        blue_arrow_positions: List[Tuple[int, int]] = [
            (150, 525),
            (150, 150),
            (200, 200),
            (200, 475),
        ]

        self.position_arrows(red_arrows, red_arrow_positions)
        self.position_arrows(blue_arrows, blue_arrow_positions)

        for motion in self.motions:
            motion.arrow.loc = motion.arrow.location_calculator.get_arrow_location()

        for arrow in arrows:
            arrow_dict = {
                COLOR: arrow.color,
            }

        return arrows

    def create_motions(self) -> None:
        motions = []
        motion_dicts: List[Dict] = [
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: PRO,
                PROP_ROT_DIR: CLOCKWISE,
                START_LOC: NORTH,
                END_LOC: EAST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: PRO,
                PROP_ROT_DIR: COUNTER_CLOCKWISE,
                START_LOC: SOUTH,
                END_LOC: EAST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: ANTI,
                PROP_ROT_DIR: CLOCKWISE,
                START_LOC: SOUTH,
                END_LOC: EAST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: ANTI,
                PROP_ROT_DIR: COUNTER_CLOCKWISE,
                START_LOC: NORTH,
                END_LOC: EAST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: PRO,
                PROP_ROT_DIR: CLOCKWISE,
                START_LOC: SOUTH,
                END_LOC: WEST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: PRO,
                PROP_ROT_DIR: COUNTER_CLOCKWISE,
                START_LOC: NORTH,
                END_LOC: WEST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: ANTI,
                PROP_ROT_DIR: CLOCKWISE,
                START_LOC: NORTH,
                END_LOC: WEST,
                TURNS: 0,
                START_ORI: IN,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                MOTION_TYPE: ANTI,
                PROP_ROT_DIR: COUNTER_CLOCKWISE,
                START_LOC: SOUTH,
                END_LOC: WEST,
                TURNS: 0,
                START_ORI: IN,
            },
        ]

        for motion_dict in motion_dicts:
            motion = Motion(self, motion_dict)
            motions.append(motion)
        return motions

    def position_arrows(
        self, arrows: List[Arrow], positions: List[Tuple[int, int]]
    ) -> None:
        for arrow, pos in zip(arrows, positions):
            arrow.setPos(*pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)
        closest_arrow = self.find_closest_arrow(scene_pos)

        if closest_arrow:
            self.target_arrow = closest_arrow
            if not self.drag:
                pictograph = (
                    self.main_widget.graph_editor_tab.graph_editor.main_pictograph
                )
                self.drag = ArrowBoxDrag(self.main_widget, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag.match_target_arrow(self.target_arrow)
                self.drag.start_drag(event_pos)
        else:
            self.target_arrow = None
            event.ignore()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.target_arrow and self.drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.drag.handle_mouse_move(event_pos)
        else:
            self.highlight_closest_arrow(event.scenePos())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.drag:
            self.drag.handle_mouse_release()
            self.target_arrow = None
        self.highlight_closest_arrow(event.scenePos())

    def find_closest_arrow(self, scene_pos: QPointF) -> "Arrow":
        closest_arrow = None
        min_distance = float("inf")
        for arrow in self.arrows:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance
        return closest_arrow

    def highlight_closest_arrow(self, cursor_pos: QPointF) -> None:
        closest_arrow = self.find_closest_arrow(cursor_pos)
        for arrow in self.arrows:
            arrow.toggle_dimmer(arrow != closest_arrow)

    def dim_all_arrows(self) -> None:
        for arrow in self.arrows:
            arrow.toggle_dimmer(True)
