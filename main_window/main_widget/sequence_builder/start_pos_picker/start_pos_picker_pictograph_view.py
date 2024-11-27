from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QSizePolicy, QApplication, QGraphicsRectItem
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QMouseEvent, QCursor, QBrush, QColor, QKeyEvent

from base_widgets.base_pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)
from base_widgets.base_pictograph.pictograph_view import PictographView
from base_widgets.base_pictograph.pictograph_view_key_event_handler import (
    PictographViewKeyEventHandler,
)
from base_widgets.base_pictograph.pictograph_view_mouse_event_handler import (
    PictographViewMouseEventHandler,
)


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.sequence_builder.option_picker.option_picker import (
        OptionPicker,
    )


class StartPosPickerPictographView(PictographView):
    original_style: str

    def __init__(
        self, pictograph: "BasePictograph", option_picker: "OptionPicker"
    ) -> None:
        super().__init__(pictograph, option_picker)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.original_style = ""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

        self.mouse_event_handler = PictographViewMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.key_event_handler = PictographViewKeyEventHandler(self)

        self._gestureInProgress = False
        self._ignoreMouseEvents = False
        self._ignoreNextMousePress = False
        self._touchTimeout = QTimer(self)
        self._touchTimeout.setSingleShot(True)
        self._touchTimeout.timeout.connect(self._resetTouchState)
        self._touchTimeout.setInterval(100)  # Adjust as needed

    ### EVENTS ###

    def set_overlay_color(self, color: str) -> None:
        overlay = QGraphicsRectItem(self.sceneRect())
        overlay.setBrush(QBrush(QColor(color)))
        overlay.setOpacity(0.5)
        self.scene().addItem(overlay)

    def set_enabled(self, enabled: bool) -> None:
        self._ignoreMouseEvents = not enabled

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.key_event_handler.handle_key_press(event):
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
        if not self.pictograph.quiz_mode:
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
        from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pictograph.container.styled_border_overlay.set_gold_border()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
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

    def resizeEvent(self, event):
        """Trigger fitInView whenever the widget is resized."""
        super().resizeEvent(event)
        self._resize_pictograph_view()

    def _resize_pictograph_view(self):
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        size = self.calculate_view_size()
        self.pictograph.container.styled_border_overlay.update_border_widths()
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMinimumHeight(size)
        self.setMaximumHeight(size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        # self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()

    def calculate_view_size(self) -> int:
        view_width = int((self.pictograph.main_widget.manual_builder.width() / 4))
        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))
        view_width = view_width - (outer_border_width) - (inner_border_width)
        return view_width
