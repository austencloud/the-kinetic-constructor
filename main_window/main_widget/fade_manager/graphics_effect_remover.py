from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from .fade_manager import FadeManager


class GraphicsEffectRemover:
    def __init__(self, fade_manager: "FadeManager"):
        self.manager = fade_manager

    def clear_graphics_effects(self, widgets: list[QWidget] = []) -> None:
        """Remove all graphics effects from widgets and their children."""
        default_widgets = [
            self.manager.main_widget.right_stack.currentWidget(),
            self.manager.main_widget.left_stack.currentWidget(),
        ]
        widgets = default_widgets
        for widget in widgets:
            if widget:
                self._remove_all_graphics_effects(widget)

    def _remove_all_graphics_effects(self, widget: QWidget):
        """Remove graphics effects recursively and reset widget visibility."""
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)
        if hasattr(widget, "children"):
            for child in widget.findChildren(QWidget):
                if child.graphicsEffect():
                    if child.__class__.__base__ != BaseIndicatorLabel:
                        child.setGraphicsEffect(None)
