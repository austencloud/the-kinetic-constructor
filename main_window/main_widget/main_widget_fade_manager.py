from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    pyqtSlot,
    QParallelAnimationGroup,
)

from main_window.main_widget.construct_tab.option_picker.option_picker import (
    OptionPicker,
)

if TYPE_CHECKING:
    from main_widget.main_widget import MainWidget


class MainWidgetFadeManager(QObject):
    """Manages fade-out/fade-in animations for your single stacked widget."""

    duration = 300

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self._old_opacity: Optional[QGraphicsOpacityEffect] = None
        self._new_opacity: Optional[QGraphicsOpacityEffect] = None
        self._is_animating = False

    def fade_to_tab(
        self,
        stack: QStackedLayout,
        new_index: int,
    ):
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

        self._fade_stack(old_index, new_index)

    def _fade_stack(self, old_index: int, new_index: int):
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

        fade_out.finished.connect(lambda: self._switch_and_fade_in(new_index))

        fade_out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _switch_and_fade_in(self, new_index: int):
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

    def fade_both_stacks_in_parallel(
        self,
        right_stack: QStackedLayout,
        right_new_index,
        left_stack: QStackedLayout,
        left_new_index,
    ):
        # 1) Gather old widgets
        old_right_idx = right_stack.currentIndex()
        old_left_idx = left_stack.currentIndex()

        if old_right_idx == right_new_index and old_left_idx == left_new_index:
            return  # Already on those pages, do nothing

        old_right_widget = right_stack.widget(old_right_idx)
        old_left_widget = left_stack.widget(old_left_idx)
        new_right_widget = right_stack.widget(right_new_index)
        new_left_widget = left_stack.widget(left_new_index)

        if not old_right_widget or not old_left_widget:
            return

        # 2) Create parallel fade-out group
        self.fade_out_group = QParallelAnimationGroup(self)  # Pass `self` as parent
    
        old_right_effect = self._ensure_opacity_effect(old_right_widget)
        old_left_effect = self._ensure_opacity_effect(old_left_widget)

        anim_out_right = QPropertyAnimation(old_right_effect, b"opacity", self)
        anim_out_right.setDuration(self.duration)
        anim_out_right.setStartValue(1.0)
        anim_out_right.setEndValue(0.0)
        anim_out_right.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_out_left = QPropertyAnimation(old_left_effect, b"opacity", self)
        anim_out_left.setDuration(self.duration)
        anim_out_left.setStartValue(1.0)
        anim_out_left.setEndValue(0.0)
        anim_out_left.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_out_group.addAnimation(anim_out_right)
        self.fade_out_group.addAnimation(anim_out_left)

        self.fade_out_group.finished.connect(
            lambda: self._switch_and_fade_in_both(
                right_stack,
                right_new_index,
                new_right_widget,
                left_stack,
                left_new_index,
                new_left_widget,
            )
        )

        self.fade_out_group.start()
        self._is_animating = True  # Mark that we’re in a fade now

    def _switch_and_fade_in_both(
        self,
        right_stack: QStackedLayout,
        right_new_index,
        new_right_widget,
        left_stack: QStackedLayout,
        left_new_index,
        new_left_widget,
    ):
        # 3) Switch each stack’s index
        right_stack.setCurrentIndex(right_new_index)
        left_stack.setCurrentIndex(left_new_index)

        # Reset old widgets’ opacity to 1 for next time
        # (if you need them to show up fully when switched back)
        # old_right_effect.setOpacity(1.0)
        # old_left_effect.setOpacity(1.0)

        # 4) Create parallel fade-in group
        self.fade_in_group = QParallelAnimationGroup()

        new_right_effect = self._ensure_opacity_effect(new_right_widget)
        new_right_effect.setOpacity(0.0)
        anim_in_right = QPropertyAnimation(new_right_effect, b"opacity", self)
        anim_in_right.setDuration(self.duration)
        anim_in_right.setStartValue(0.0)
        anim_in_right.setEndValue(1.0)
        anim_in_right.setEasingCurve(QEasingCurve.Type.InOutQuad)

        new_left_effect = self._ensure_opacity_effect(new_left_widget)
        new_left_effect.setOpacity(0.0)
        anim_in_left = QPropertyAnimation(new_left_effect, b"opacity", self)
        anim_in_left.setDuration(self.duration)
        anim_in_left.setStartValue(0.0)
        anim_in_left.setEndValue(1.0)
        anim_in_left.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_in_group.addAnimation(anim_in_right)
        self.fade_in_group.addAnimation(anim_in_left)

        self.fade_in_group.finished.connect(self._on_fade_in_finished)
        self.fade_in_group.start()
