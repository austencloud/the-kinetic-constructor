import logging
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel
from main_window.main_widget.fade_manager.fadeable_opacity_effect import FadableOpacityEffect

if TYPE_CHECKING:
    from .fade_manager import FadeManager


class GraphicsEffectRemover:
    def __init__(self, fade_manager: "FadeManager"):
        self.manager = fade_manager

    def clear_graphics_effects(self, widgets: list[QWidget] = None) -> None:
        """Remove all graphics effects from specified widgets and their children."""
        if not widgets:  # Handle None or empty list
            widgets = [
                self.manager.main_widget.right_stack.currentWidget(),
                self.manager.main_widget.left_stack.currentWidget(),
            ]
        for widget in widgets:
            if widget:
                self._remove_all_graphics_effects(widget)

    def _remove_all_graphics_effects(self, widget):
        if isinstance(widget, BaseIndicatorLabel):
            # Do nothing; let it keep its effect
            return
        # If widget is a QWidget, process its graphics effect and its children.
        if isinstance(widget, QWidget):
            if widget.graphicsEffect():
                print(f"Removing effect from widget: {widget.objectName()}")
                widget.setGraphicsEffect(None)
            for child in widget.findChildren(QWidget):
                if child.graphicsEffect():
                    print(f"Removing effect from child widget: {child.objectName()}")
                    child.setGraphicsEffect(None)
        else:
            # For non-QWidget items (e.g. QGraphicsItemGroup), you might choose to do nothing,
            # or handle them in a custom way.
            pass
