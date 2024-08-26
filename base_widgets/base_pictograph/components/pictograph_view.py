from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QMouseEvent, QCursor

from .pictograph_context_menu_handler import PictographContextMenuHandler
from .pictograph_view_mouse_event_handler import PictographViewMouseEventHandler


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    original_style: str

    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.original_style = ""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)
        self.mouse_event_handler = PictographViewMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self._gestureInProgress = False
        self._ignoreMouseEvents = False
        self._ignoreNextMousePress = False
        self._touchTimeout = QTimer(self)
        self._touchTimeout.setSingleShot(True)
        self._touchTimeout.timeout.connect(self._resetTouchState)
        self._touchTimeout.setInterval(100)  # Adjust as needed

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
        sections = self.pictograph.scroll_area.section_manager.sections
        letter_type = self.pictograph.letter_type

        view_width = min(
            int(
                (self.pictograph.scroll_area.option_picker.width() / COLUMN_COUNT)
                - ((sections[letter_type].pictograph_frame.spacing))
            ),
            # get the height of the option picker widget  divided by 6
            int(self.pictograph.scroll_area.option_picker.height() / 8),
        )

        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))
        view_width = view_width - (outer_border_width) - (inner_border_width)
        return view_width

    ### EVENTS ###

    def set_enabled(self, enabled: bool) -> None:
        self._ignoreMouseEvents = not enabled

    def wheelEvent(self, event) -> None:
        if self.pictograph.scroll_area:
            self.pictograph.scroll_area.wheelEvent(event)

    def keyPressEvent(self, event) -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        wasd_manager = self.pictograph.wasd_manager

        if event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph, event.key(), shift_held, ctrl_held
            )

        elif event.key() == Qt.Key.Key_X:
            wasd_manager.rotation_angle_override_manager.handle_rotation_angle_override()
        elif event.key() == Qt.Key.Key_Z:
            wasd_manager.handle_special_placement_removal()

        elif event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.pictograph.main_widget.special_placement_loader.refresh_placements()

        elif event.key() == Qt.Key.Key_C:
            wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                event.key()
            )
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        settings_manager = self.pictograph.main_widget.main_window.settings_manager
        current_prop_type = settings_manager.global_settings.get_prop_type()

        if (
            self.pictograph.prop_type != current_prop_type
            and self.pictograph.__class__.__name__ != "GE_BlankPictograph"
        ):
            settings_manager.global_settings.prop_type_changer.replace_props(
                current_prop_type, self.pictograph
            )
        settings_manager.visibility.glyph_visibility_manager.apply_current_visibility_settings(
            self.pictograph
        )

    def _resetTouchState(self) -> None:
        self._ignoreNextMousePress = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if self._ignoreMouseEvents or self._ignoreNextMousePress:
            event.ignore()
            return
        elif event.button() == Qt.MouseButton.LeftButton:
            self.mouse_event_handler.handle_mouse_press(event)
        QApplication.restoreOverrideCursor()

    def enterEvent(self, event: QEvent) -> None:
        from main_window.main_widget.top_builder_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pictograph.container.styled_border_overlay.set_gold_border()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        from main_window.main_widget.top_builder_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
            if self.mouse_event_handler.is_arrow_under_cursor(event):
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pictograph.container.styled_border_overlay.reset_border()
