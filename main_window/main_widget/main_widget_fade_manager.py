# main_widget_fade_manager.py

from typing import Optional, Callable
from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtSlot
from PyQt6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect

class MainWidgetFadeManager(QObject):
    """Manages fade-out and fade-in animations for the main widget's QStackedWidget."""
    def __init__(self, stacked_widget: QStackedWidget, duration: int = 350) -> None:
        super().__init__(stacked_widget)
        self.stacked_widget = stacked_widget
        self.duration = duration
        self.opacity_effect = QGraphicsOpacityEffect(self.stacked_widget)
        self.stacked_widget.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self._is_animating = False

    def fade_to_tab(self, new_index: int, on_finished: Optional[Callable] = None) -> None:
        """Fades out the current tab and fades in the new tab."""
        if self._is_animating or new_index == self.stacked_widget.currentIndex():
            return

        self._is_animating = True

        # Fade-out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(self.duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(lambda: self._switch_tab(new_index, on_finished))
        self.fade_out.finished.connect(self._animation_finished)
        self.fade_out.start()

    def _switch_tab(self, new_index: int, on_finished: Optional[Callable]) -> None:
        """Switches to the new tab and initiates the fade-in animation."""
        self.stacked_widget.setCurrentIndex(new_index)

        # Fade-in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(self.duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if on_finished:
            self.fade_in.finished.connect(on_finished)

        self.fade_in.finished.connect(self._animation_finished)
        self.fade_in.start()

    @pyqtSlot()
    def _animation_finished(self) -> None:
        """Resets the animation flag after completion."""
        self._is_animating = False
