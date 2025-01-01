from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QStackedWidget
from PyQt6.QtCore import QObject

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel
from .widget_fader import WidgetFader
from .stack_fader import StackFader
from .parallel_stack_fader import ParallelStackFader

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class FadeManager(QObject):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.widget_fader = WidgetFader(self)
        self.stack_fader = StackFader(self)
        self.parallel_stack_fader = ParallelStackFader(self)

    def clear_graphics_effects(self, widgets: List[QWidget]) -> None:
        """Remove all graphics effects from widgets and their children."""
        widgets = [
            self.parallel_stack_fader.right_old_widget,
            self.parallel_stack_fader.left_old_widget,
            self.parallel_stack_fader.right_new_widget,
            self.parallel_stack_fader.left_new_widget,
        ] + widgets

        for widget in widgets:
            if widget:
                self._remove_all_graphics_effects(widget)

    def _remove_all_graphics_effects(self, widget: QWidget):
        """Remove graphics effects recursively and reset widget visibility."""
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)

        for child in widget.findChildren(QWidget):
            if child.graphicsEffect():
                if child.__class__.__base__ != BaseIndicatorLabel:
                    child.setGraphicsEffect(None)

    def fade_and_update(
        self,
        widgets_to_fade: list[QWidget],
        update_callback: callable,
        duration: int = 300,
    ) -> None:
        """Fades out widgets, invokes an update callback, and fades them back in."""

        def on_fade_out_finished():
            self.clear_graphics_effects(widgets_to_fade)
            update_callback()
            self.widget_fader.fade_widgets(widgets_to_fade, True, duration)

        self.widget_fader.fade_widgets(
            widgets_to_fade, False, duration, on_fade_out_finished
        )
