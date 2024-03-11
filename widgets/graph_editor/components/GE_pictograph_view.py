from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QKeyEvent

from widgets.sequence_widget.sequence_beat_frame.beat import Beat

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_pictograph_view import GE_BlankPictograph


class GE_PictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", blank_pictograph: "GE_BlankPictograph"
    ) -> None:
        super().__init__(blank_pictograph)
        self.GE = GE
        self.is_start_pos = False
        self.blank_pictograph = blank_pictograph
        self.main_widget = GE.main_widget
        self.setScene(blank_pictograph)
        self.setFrameShape(PictographView.Shape.Box)

    def resize_GE_pictograph_view(self):
        container_height = self.GE.GE_pictograph_container.height()
        # This is not the most elegant way to do this.
        self.setMinimumHeight(int(container_height * 0.99))
        self.setMinimumWidth(int(container_height * 0.99))

        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.blank_pictograph)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        pen = QPen(Qt.GlobalColor.black, 0)
        painter.setPen(pen)

        right_edge = self.viewport().width() - 1
        painter.drawLine(right_edge, 0, right_edge, self.viewport().height())
        overlay_color = QColor("gold")
        overlay_pen = QPen(overlay_color, 4)
        overlay_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(overlay_pen)

        overlay_rect = (
            self.viewport()
            .rect()
            .adjusted(
                overlay_pen.width() // 2,
                overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
            )
        )
        painter.drawRect(overlay_rect)

    def get_current_pictograph(self) -> Pictograph:
        return self.scene()

    def set_scene(self, beat: "Beat"):
        self.setScene(beat)
        self.pictograph = beat
        if beat.view.is_start_pos:
            self.is_start_pos = True
        else:
            self.is_start_pos = False

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.pictograph.wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph, event.key(), shift_held, ctrl_held
            )

        elif event.key() == Qt.Key.Key_X:
            self.pictograph.wasd_manager.rotation_angle_override_manager.handle_rotation_angle_override(
                event.key()
            )
        elif event.key() == Qt.Key.Key_Z:
            self.pictograph.wasd_manager.handle_special_placement_removal()

        elif event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.pictograph.main_widget.special_placement_loader.refresh_placements()

        elif event.key() == Qt.Key.Key_C:
            self.pictograph.wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                event.key()
            )
        super().keyPressEvent(event)


class GE_BlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)
        self.is_blank = True
