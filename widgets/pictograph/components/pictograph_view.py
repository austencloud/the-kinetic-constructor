from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.setScene(self.pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_for_scroll_area(self) -> None:
        view_width = int(
            (
                self.pictograph.scroll_area.width()
                / self.pictograph.scroll_area.display_manager.COLUMN_COUNT
            )
            - self.pictograph.scroll_area.display_manager.SPACING
            - 10
        )
        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)

        self.view_scale = view_width / self.pictograph.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event) -> None:
        self.pictograph.scroll_area.wheelEvent(event)

    def keyPressEvent(self, event) -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.pictograph.wasd_manager.movement_manager.handle_arrow_movement(
                event.key(), shift_held
            )

        elif event.key() == Qt.Key.Key_X:
            self.pictograph.wasd_manager.rotation_manager.handle_rotation_angle_override(
                event.key()
            )

        else:
            super().keyPressEvent(event)
