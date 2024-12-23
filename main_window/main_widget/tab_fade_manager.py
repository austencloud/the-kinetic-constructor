from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
    pyqtSlot,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class TabFadeManager(QObject):
    """Manages fade-out/fade-in animations for top-level or sub-level stacked widgets."""

    duration = 370

    def __init__(self, mw: "MainWidget"):
        """Initialize TabFadeManager with references to relevant stacked widgets."""
        super().__init__(mw.main_stacked_widget)

        self.mw = mw
        # References to the top-level stacked widget and sub-stacks
        self.main_stack = mw.main_stacked_widget

        # We'll store the old/new widget opacities here:
        self._old_widget_opacity: Optional[QGraphicsOpacityEffect] = None
        self._new_widget_opacity: Optional[QGraphicsOpacityEffect] = None

        self._animation_group: Optional[QSequentialAnimationGroup] = None
        self._is_animating = False  # Flag to track animation state

    def fade_to_tab(self, new_index: int, on_finished: Optional[Callable] = None):
        """
        Fades out the relevant old widget and fades in the new widget
        based on the user’s new tab choice (new_index).

        The new_index maps to:
          0 -> Build
          1 -> Generate
          2 -> Dictionary
          3 -> Learn
          4 -> Act

        We'll decide whether to animate the main_stack or one of the sub-stacks.
        """
        if self._is_animating:
            return  # Prevent starting another animation
        # 1) Determine top-level index + sub-level index from new_index
        #    (matching your existing logic in MainWidgetTabs)
        if new_index in [0, 1]:
            main_idx = 0
        elif new_index == 2:
            main_idx = 1
        elif new_index == 3:
            main_idx = 2
        elif new_index == 4:
            main_idx = 3

        # 4) Actually do the fade:
        self._fade_stack(main_idx, on_finished)

    def _fade_stack(
        self,
        main_idx: int,
        on_finished: Optional[Callable] = None,
    ):
        """
        Fades out the current widget in `stack_widget`, then switches to the new
        page (main_idx/sub_idx), and fades in the new widget.
        If sub_idx is None, it means a single-level stack switch (like going to Act tab).
        """
        self._is_animating = True  # Set the flag

        old_idx = self.main_stack.currentIndex()
        old_widget = self.main_stack.widget(old_idx)

        new_idx = main_idx

        # If top-level, just do new_idx = main_idx
        # If sub-level, do new_idx = sub_idx

        new_widget = self.main_stack.widget(new_idx)
        if not old_widget or not new_widget:
            return

        # Ensure each has an opacity effect
        self._old_widget_opacity = self._ensure_opacity_effect(old_widget)
        self._new_widget_opacity = self._ensure_opacity_effect(new_widget)

        # Fade-out animation
        fade_out = QPropertyAnimation(self._old_widget_opacity, b"opacity", self)
        fade_out.setDuration(self.duration)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Chain fade-out → fade-in
        fade_out.finished.connect(
            lambda: self._switch_and_fade_in(self.main_stack, new_idx, on_finished)
        )
        fade_out.finished.connect(
            self._animation_finished
        )  # Reset flag after animation
        fade_out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _switch_and_fade_in(
        self,
        stack_widget: QStackedWidget,
        new_idx: int,
        on_finished: Optional[Callable],
    ):
        """
        Switches stack_widget to new_idx, then fades in the new widget from 0 → 1.
        """
        old_idx = stack_widget.currentIndex()
        old_widget = stack_widget.widget(old_idx)
        # Hide old widget if needed
        if old_widget and self._old_widget_opacity:
            self._old_widget_opacity.setOpacity(1.0)  # Restore opacity for next time
            old_widget.hide()

        # Switch to new index
        stack_widget.setCurrentIndex(new_idx)
        new_widget = stack_widget.widget(new_idx)
        if new_widget and self._new_widget_opacity:
            self._new_widget_opacity.setOpacity(0.0)
            new_widget.show()

        # Fade-in animation
        fade_in = QPropertyAnimation(self._new_widget_opacity, b"opacity", self)
        fade_in.setDuration(self.duration)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if on_finished:
            fade_in.finished.connect(on_finished)

        # After fade-in finishes, reset the flag
        fade_in.finished.connect(self._animation_finished)

        fade_in.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _animation_finished(self):
        self._is_animating = False  # Reset the flag

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Ensures a QGraphicsOpacityEffect is present on the widget, returning it."""
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect
