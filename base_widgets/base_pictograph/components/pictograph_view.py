from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QSizePolicy, QApplication, QGraphicsRectItem
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QMouseEvent, QCursor, QBrush, QColor

from .pictograph_context_menu_handler import PictographContextMenuHandler
from .pictograph_view_mouse_event_handler import PictographViewMouseEventHandler

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.original_style = ""
        self._gesture_in_progress = False
        self._ignore_mouse_events = False
        self._ignore_next_mouse_press = False
        self.settings_manager = self.pictograph.main_widget.main_window.settings_manager
        self.wasd_manager = self.pictograph.wasd_manager

        # Event Handlers
        self.mouse_event_handler = PictographViewMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)

        # Timer for touch gestures
        self._touch_timeout = QTimer(self)
        self._touch_timeout.setSingleShot(True)
        self._touch_timeout.timeout.connect(self._reset_touch_state)
        self._touch_timeout.setInterval(100)

        self._setup_view_properties()

    ### INITIALIZATION METHODS ###
    def _setup_view_properties(self) -> None:
        """Set up properties for the view, such as scrollbars and size policy."""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

    ### RESIZE METHODS ###
    def resize_pictograph_view(self) -> None:
        """Resize the view and scale it according to the calculated width."""
        view_width = self._calculate_view_width()
        self._adjust_view_dimensions(view_width)
        self._scale_view(view_width)
        self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()

    def _calculate_view_width(self) -> int:
        """Calculate the appropriate width for the view based on the pictograph's properties."""
        column_count = self.pictograph.scroll_area.display_manager.COLUMN_COUNT
        sections = self.pictograph.scroll_area.section_manager.sections
        letter_type = self.pictograph.letter_type

        option_picker_width = (
            self.pictograph.scroll_area.option_picker.main_widget.width() // 2
        )
        option_picker_height = self.pictograph.scroll_area.option_picker.height() // 8
        spacing = sections[letter_type].pictograph_frame.spacing

        view_width = min(
            option_picker_width // column_count - spacing, option_picker_height
        )

        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))
        return view_width - outer_border_width - inner_border_width

    def _adjust_view_dimensions(self, view_width: int) -> None:
        """Set the minimum and maximum dimensions for the view."""
        self.setFixedSize(view_width, view_width)

    def _scale_view(self, view_width: int) -> None:
        """Reset and apply the scaling transformation to the view."""
        self.view_scale = view_width / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    ### EVENT HANDLERS ###
    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if self._ignore_mouse_events or self._ignore_next_mouse_press:
            event.ignore()
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_event_handler.handle_mouse_press(event)
        QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        is_in_graph_editor = self._is_in_graph_editor_container()
        if is_in_graph_editor and self.mouse_event_handler.is_arrow_under_cursor(event):
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def keyPressEvent(self, event) -> None:
        key = event.key()
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ctrl_held = event.modifiers() & Qt.KeyboardModifier.ControlModifier

        # WASD or other key management handled cleanly
        self._handle_wasd_keys(key, shift_held, ctrl_held)
        self._handle_special_keys(key)

    def _handle_wasd_keys(self, key, shift_held, ctrl_held) -> None:
        """Handle movement-related key events."""
        if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.wasd_manager.movement_manager.handle_arrow_movement(
                self.pictograph, key, shift_held, ctrl_held
            )

    def _handle_special_keys(self, key) -> None:
        """Handle special key events such as rotation, prop placement, etc."""
        if key == Qt.Key.Key_X:
            self.wasd_manager.rotation_angle_override_manager.handle_rotation_angle_override()
        elif key == Qt.Key.Key_Z:
            self.wasd_manager.handle_special_placement_removal()
        elif key == Qt.Key.Key_Q or key == Qt.Key.Key_F5:
            self.pictograph.main_widget.special_placement_loader.refresh_placements()
        elif key == Qt.Key.Key_C:
            self.wasd_manager.prop_placement_override_manager.handle_prop_placement_override(
                key
            )

    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(self._get_cursor_type())
        self.pictograph.container.styled_border_overlay.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pictograph.container.styled_border_overlay.reset_border()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self._should_replace_props():
            self._replace_props()

    def wheelEvent(self, event) -> None:
        if self.pictograph.scroll_area:
            self.pictograph.scroll_area.wheelEvent(event)

    ### UTILITY METHODS ###
    def _get_cursor_type(self) -> QCursor:
        """Determine the cursor type based on the context."""
        if self._is_in_graph_editor_container():
            return QCursor(Qt.CursorShape.ArrowCursor)
        return QCursor(Qt.CursorShape.PointingHandCursor)

    def _is_in_graph_editor_container(self) -> bool:
        """Check if the view's parent is a Graph Editor Pictograph Container."""
        from main_window.main_widget.top_builder_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        return isinstance(self.parent(), GraphEditorPictographContainer)

    def _should_replace_props(self) -> bool:
        """Check if the prop type needs to be replaced based on current settings."""
        current_prop_type = self.settings_manager.global_settings.get_prop_type()
        return (
            self.pictograph.prop_type != current_prop_type
            and self.pictograph.__class__.__name__ != "GE_BlankPictograph"
        )

    def _replace_props(self) -> None:
        """Replace props in the pictograph according to the global settings."""
        current_prop_type = self.settings_manager.global_settings.get_prop_type()
        self.settings_manager.global_settings.prop_type_changer.replace_props(
            current_prop_type, self.pictograph
        )

    def set_overlay_color(self, color: str) -> None:
        """Create and apply a semi-transparent overlay to the view."""
        overlay = QGraphicsRectItem(self.sceneRect())
        overlay.setBrush(QBrush(QColor(color)))
        overlay.setOpacity(0.5)
        self.scene().addItem(overlay)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the view based on the flag."""
        self._ignore_mouse_events = not enabled

    def _reset_touch_state(self) -> None:
        """Reset touch-related states after a timeout."""
        self._ignore_next_mouse_press = False

    def resizeEvent(self, event) -> None:
        """Ensure the view is properly resized and scaled when the widget size changes."""
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()
