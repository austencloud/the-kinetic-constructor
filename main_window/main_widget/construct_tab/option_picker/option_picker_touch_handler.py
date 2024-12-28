from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from .option_picker_pictograph_view import OptionPickerPictographView


class OptionPickerTouchHandler:
    def __init__(self, view: "OptionPickerPictographView") -> None:
        self.view = view
        self._gestureInProgress = False
        self._ignoreMouseEvents = False
        self._ignoreNextMousePress = False
        self._touchTimeout = QTimer(self.view)
        self._touchTimeout.setSingleShot(True)
        self._touchTimeout.timeout.connect(self._resetTouchState)
        self._touchTimeout.setInterval(100)

    def set_enabled(self, enabled: bool) -> None:
        self._ignoreMouseEvents = not enabled

    def _resetTouchState(self) -> None:
        self._ignoreNextMousePress = False

    def handle_mouse_press(self, event: QMouseEvent) -> bool:
        if self._ignoreMouseEvents or self._ignoreNextMousePress:
            event.ignore()
            return False
        elif event.button() == Qt.MouseButton.LeftButton:
            self.view.click_handler.on_option_clicked(self.view.pictograph)
        return True

