from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from constants import BLUE, IG_PICTOGRAPH, RED
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt

from utilities.TypeChecking.TypeChecking import Colors
from widgets.ig_tab.wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager
if TYPE_CHECKING:
    from widgets.scroll_area.scroll_area import ScrollArea


class IGPictograph(Pictograph):
    def __init__(self, main_widget, scroll_area: "ScrollArea") -> None:
        super().__init__(main_widget, IG_PICTOGRAPH)
        self.view: IGPictographView = IGPictographView(self)
        self.ig_scroll_area = scroll_area
        self.selected_arrow = None
        self.wasd_adjustment_manager = WASD_AdjustmentManager(self)


class IGPictographView(QGraphicsView):
    def __init__(self, ig_pictograph: IGPictograph) -> None:
        super().__init__(ig_pictograph)
        self.ig_pictograph = ig_pictograph
        self.setScene(self.ig_pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_for_scroll_area(self) -> None:
        view_width = int(
            (
                self.ig_pictograph.ig_scroll_area.width()
                / self.ig_pictograph.ig_scroll_area.display_manager.COLUMN_COUNT
            )
            - self.ig_pictograph.ig_scroll_area.display_manager.SPACING
            - 10
        )
        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)

        self.view_scale = view_width / self.ig_pictograph.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event) -> None:
        self.ig_pictograph.ig_scroll_area.wheelEvent(event)

    def keyPressEvent(self, event) -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.ig_pictograph.wasd_adjustment_manager.movement_manager.handle_arrow_movement(
                event.key(), shift_held
            )

        elif event.key() == Qt.Key.Key_X:
            self.ig_pictograph.wasd_adjustment_manager.rotation_manager.handle_rotation_angle_override(
                event.key()
            )

        else:
            super().keyPressEvent(event)
