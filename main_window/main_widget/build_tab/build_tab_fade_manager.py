# build_tab_fade_manager.py

from typing import Optional, Callable
from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtSlot
from PyQt6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect

class BuildTabFadeManager(QObject):
    duration = 350  # Duration in milliseconds

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__(stacked_widget)
        self.stacked_widget = stacked_widget
        self.opacity_effect = QGraphicsOpacityEffect(self.stacked_widget)
        self.stacked_widget.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self._is_animating = False

    def fade_to_tab(self, new_index: int) -> None:
        if self._is_animating or new_index == self.stacked_widget.currentIndex():
            return

        self._is_animating = True

        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(self.duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(lambda: self._switch_tab(new_index))
        self.fade_out.finished.connect(self._start_fade_in)
        self.fade_out.finished.connect(self._animation_finished)
        self.fade_out.start()

    def _switch_tab(self, new_index: int) -> None:
        self.stacked_widget.setCurrentIndex(new_index)

    def _start_fade_in(self) -> None:
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(self.duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.start()

    @pyqtSlot()
    def _animation_finished(self) -> None:
        self._is_animating = False
