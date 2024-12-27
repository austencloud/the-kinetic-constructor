from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    pyqtSlot,
)

if TYPE_CHECKING:
    from main_widget.main_widget import MainWidget


class TabFadeManager(QObject):
    """Manages fade-out/fade-in animations for your single stacked widget."""

    duration = 370

    def __init__(self, mw: "MainWidget"):
        super().__init__(mw)
        self.mw = mw
        self._old_opacity: Optional[QGraphicsOpacityEffect] = None
        self._new_opacity: Optional[QGraphicsOpacityEffect] = None
        self._is_animating = False

    def fade_to_tab(self, stack:QStackedLayout, new_index: int, on_finished: Optional[Callable] = None):
        """
        new_index corresponds to the pages in mw.content_stack:
          0 -> Build
          1 -> Generate
          2 -> Browse
          3 -> Learn
          4 -> Write
        """
        if self._is_animating:
            return
        self.stack = stack
        old_index = self.stack.currentIndex()
        if old_index == new_index:
            return  # Already on that page

        self._fade_stack(old_index, new_index, on_finished)

    def _fade_stack(
        self,
        old_index: int,
        new_index: int,
        on_finished: Optional[Callable] = None
    ):
        self._is_animating = True

        old_widget = self.stack.widget(old_index)
        new_widget = self.stack.widget(new_index)
        if not old_widget or not new_widget:
            return

        self._old_opacity = self._ensure_opacity_effect(old_widget)
        self._new_opacity = self._ensure_opacity_effect(new_widget)

        # Fade out
        fade_out = QPropertyAnimation(self._old_opacity, b"opacity", self)
        fade_out.setDuration(self.duration)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        fade_out.finished.connect(
            lambda: self._switch_and_fade_in(new_index, on_finished)
        )

        fade_out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _switch_and_fade_in(self, new_index: int, on_finished: Optional[Callable]):
        # Switch stack page
        self.stack.setCurrentIndex(new_index)

        # Reset the old widget to full opacity so next time it fades out properly
        if self._old_opacity:
            self._old_opacity.setOpacity(1.0)

        new_widget = self.stack.currentWidget()
        if new_widget and self._new_opacity:
            self._new_opacity.setOpacity(0.0)

        # Fade in
        fade_in = QPropertyAnimation(self._new_opacity, b"opacity", self)
        fade_in.setDuration(self.duration)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if on_finished:
            fade_in.finished.connect(on_finished)

        fade_in.finished.connect(self._on_fade_in_finished)
        fade_in.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _on_fade_in_finished(self):
        self._is_animating = False

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect
