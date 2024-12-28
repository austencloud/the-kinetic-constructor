from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, QTimer, Qt
from PyQt6.QtGui import QMouseEvent

if TYPE_CHECKING:
    from .option_picker_pictograph_view import OptionPickerPictographView


class OptionPickerTouchHandler(QObject):
    """
    Handles touch/gesture states for an OptionPickerPictographView.
    Keeps track of _gestureInProgress, _ignoreMouseEvents, etc.
    """

    def __init__(self, parent_view: "OptionPickerPictographView"):
        super().__init__(parent_view)
        self.view = parent_view

        # State flags
        self._gestureInProgress = False
        self._ignoreMouseEvents = False
        self._ignoreNextMousePress = False

        # Timer for resetting touch state
        self._touchTimeout = QTimer(self)
        self._touchTimeout.setSingleShot(True)
        self._touchTimeout.setInterval(100)
        self._touchTimeout.timeout.connect(self._resetTouchState)

        # Grab gestures for the view
        self.view.grabGesture(Qt.GestureType.TapGesture)
        self.view.grabGesture(Qt.GestureType.TapAndHoldGesture)

    def set_enabled(self, enabled: bool) -> None:
        """
        If disabled, we ignore all mouse/touch events for this pictograph.
        """
        self._ignoreMouseEvents = not enabled

    def on_mouse_press_event(self, event: QMouseEvent) -> bool:
        """
        Called from the parent view's mousePressEvent.
        Returns True if event is handled (or should be ignored), False otherwise.
        """
        if self._ignoreMouseEvents or self._ignoreNextMousePress:
            event.ignore()
            return True  # We "handled" it by ignoring

        # We didn't ignore, so let the view handle it
        return False

    def start_touch_timeout(self):
        """
        Possibly called if you need to start the timer indicating a short
        'touch state' after e.g. a TapGesture was recognized.
        """
        self._touchTimeout.start()

    def _resetTouchState(self) -> None:
        self._ignoreNextMousePress = False
        self._gestureInProgress = False

    # If you need a 'gestureInProgress' setter or other methods, add them:
    def set_gesture_in_progress(self, in_progress: bool):
        self._gestureInProgress = in_progress
