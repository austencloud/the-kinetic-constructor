from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QSizePolicy
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QTouchEvent

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographView(QGraphicsView):
    original_style: str

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.original_style = ""
        self.setScene(self.pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def resize_pictograph_view(self) -> None:
        view_width = self.calculate_view_width()
        self.pictograph.container.styled_border_overlay.update_border_widths()
        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()

    def calculate_view_width(self):
        COLUMN_COUNT = self.pictograph.scroll_area.display_manager.COLUMN_COUNT
        sections = self.pictograph.scroll_area.sections_manager.sections
        letter_type = self.pictograph.letter_type
        view_width = int(
            (self.pictograph.scroll_area.width() / COLUMN_COUNT)
            - ((sections[letter_type].pictograph_frame.spacing))
        )
        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))
        view_width = view_width - (outer_border_width) - (inner_border_width)
        return view_width

    def wheelEvent(self, event) -> None:
        self.pictograph.scroll_area.wheelEvent(event)

    def enterEvent(self, event: QEvent) -> None:

        self.pictograph.container.styled_border_overlay.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.pictograph.container.styled_border_overlay.reset_border()

    def keyPressEvent(self, event) -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.pictograph.wasd_manager.movement_manager.handle_arrow_movement(
                event.key(), shift_held, ctrl_held
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
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        settings_manager = self.pictograph.main_widget.main_window.settings_manager
        current_prop_type = settings_manager.get_prop_type()

        if (
            self.pictograph.prop_type != current_prop_type
            and self.pictograph.__class__.__name__ != "GraphEditorPictograph"
        ):
            settings_manager.prop_type_changer.replace_props(
                current_prop_type, self.pictograph
            )
        settings_manager.glyph_visibility_manager.apply_current_visibility_settings(
            self.pictograph
        )

    def touchEvent(self, event):
        touch_points = event.touchPoints()
        for point in touch_points:
            pos = point.pos()
            if event.type() == QEvent.Type.TouchBegin:
                self.update_border_for_touch_position(pos)
            elif event.type() == QEvent.Type.TouchUpdate:
                self.update_border_for_touch_position(pos)
            elif event.type() == QEvent.Type.TouchEnd:
                self.trigger_pictograph_action(pos)

    def update_border_for_touch_position(self, pos):
        # Convert touch point position to view coordinates
        local_pos = self.mapFromGlobal(pos.toPoint())
        # Implement logic to find and highlight the pictograph under the touch position
        pass

    def trigger_pictograph_action(self, pos):
        # Convert touch point position to view coordinates
        local_pos = self.mapFromGlobal(pos.toPoint())
        # Implement logic to determine which pictograph is under 'pos' and trigger its action
        pass
