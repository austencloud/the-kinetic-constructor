from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QWidget
if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.widget_fader import WidgetFader


class FadeWhenReadyHelper(QObject):
    def __init__(
        self,
        widget: QWidget,
        fade_in: bool,
        duration: int,
        callback: Optional[callable],
        fader: "WidgetFader",
    ):
        super().__init__(widget)
        self.widget = widget
        self.fade_in = fade_in
        self.duration = duration
        self.callback = callback
        self.fader = fader

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Show:
            # Remove this event filter, then trigger the fade.
            obj.removeEventFilter(self)
            self.fader.fade_widgets([obj], self.fade_in, self.duration, self.callback)
            return True
        return False
