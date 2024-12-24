# tab_fade_manager.py
from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    pyqtSlot,
)
import logging

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class TabFadeManager(QObject):
    """Manages fade-out/fade-in animations for primary stacked widgets."""

    duration = 350

    def __init__(self, mw: "MainWidget"):
        super().__init__(mw.main_stacked_widget)
        self.mw = mw
        self.main_stack = mw.main_stacked_widget

        # Opacity effect for main_stack
        self.opacity_effect = QGraphicsOpacityEffect(self.main_stack)
        self.main_stack.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)  # Fully visible initially

        # Animation state flag
        self._is_animating = False

    def fade_to_tab(self, new_index: int, on_finished: Optional[Callable] = None):
        """Fades out the current tab and fades in the new tab."""
        if self._is_animating:
            logging.debug("Fade animation already in progress.")
            return  # Prevent overlapping animations

        if new_index == self.main_stack.currentIndex():
            logging.debug("Selected tab is already active. No fade needed.")
            return  # No need to fade if the same tab is selected

        self._is_animating = True

        # Fade-out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(self.duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Connect fade-out finished signal to switch tab and start fade-in
        self.fade_out.finished.connect(lambda: self._switch_tab(new_index, on_finished))
        self.fade_out.finished.connect(self._animation_finished)

        # Start fade-out
        self.fade_out.start()

    def _switch_tab(self, new_index: int, on_finished: Optional[Callable]):
        """Switch to the new tab and initiate fade-in."""
        self.main_stack.setCurrentIndex(new_index)

        # Start fade-in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(self.duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if on_finished:
            self.fade_in.finished.connect(on_finished)

        # After fade-in finishes, reset the animation flag
        self.fade_in.finished.connect(self._animation_finished)

        # Start fade-in
        self.fade_in.start()

    @pyqtSlot()
    def _animation_finished(self):
        """Resets the animation flag after completion."""
        self._is_animating = False
