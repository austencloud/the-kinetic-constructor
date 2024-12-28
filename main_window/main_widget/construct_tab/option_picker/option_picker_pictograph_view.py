from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QMouseEvent, QCursor, QKeyEvent

from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView
from base_widgets.base_pictograph.pictograph_view_key_event_handler import (
    PictographViewKeyEventHandler,
)
from .option_picker_touch_handler import OptionPickerTouchHandler
from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
    GraphEditorPictographContainer,
)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from .option_picker import OptionPicker


class OptionPickerPictographView(BorderedPictographView):
    def __init__(
        self, pictograph: "BasePictograph", option_picker: "OptionPicker"
    ) -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.option_picker = option_picker
        self.click_handler = self.option_picker.construct_tab.option_click_handler

        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

        self.key_event_handler = PictographViewKeyEventHandler(self)
        self.touch_handler = OptionPickerTouchHandler(self)

    ### EVENTS ###

    def set_enabled(self, enabled: bool) -> None:
        self.touch_handler.set_enabled(enabled)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.key_event_handler.handle_key_press(event):
            super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if not self.touch_handler.handle_mouse_press(event):
            return
        QApplication.restoreOverrideCursor()

    def enterEvent(self, event: QEvent) -> None:
        if isinstance(self.parent(), GraphEditorPictographContainer):
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pictograph.view.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pictograph.view.reset_border()
