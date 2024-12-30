from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QStackedLayout, QApplication
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    pyqtSlot,
    QParallelAnimationGroup,
)

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_widget.main_widget import MainWidget


class FadeManager(QObject):
    """Manages fade-out/fade-in animations for your single stacked widget."""

    old_widget: Optional[QWidget] = None
    new_widget: Optional[QWidget] = None
    new_right_widget: Optional[QWidget] = None
    new_left_widget: Optional[QWidget] = None
    duration = 300
    _old_opacity: Optional[QGraphicsOpacityEffect] = None
    _new_opacity: Optional[QGraphicsOpacityEffect] = None
    _is_animating = False

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget

    def fade_to_tab(self, stack: QStackedLayout, new_index: int, callback: callable = None):
        if self._is_animating:
            return

        self.stack = stack
        old_index = self.stack.currentIndex()
        if old_index == new_index:
            return

        self._is_animating = True

        self.old_widget = self.stack.widget(old_index)
        self.new_widget = self.stack.widget(new_index)
        if not self.old_widget or not self.new_widget:
            return

        for i in range(self.stack.count()):
            widget = self.stack.widget(i)
            self.clear_graphics_effects(widget)

        self._old_opacity = self._ensure_opacity_effect(self.old_widget)
        self._new_opacity = self._ensure_opacity_effect(self.new_widget)

        self.fade_out = QPropertyAnimation(self._old_opacity, b"opacity", self)
        self.fade_out.setDuration(self.duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_out.finished.connect(lambda: self._switch_and_fade_in(new_index, callback))
        self.fade_out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def _switch_and_fade_in(self, new_index: int, callback: callable = None):
        self.stack.setCurrentIndex(new_index)
        if callback:
            callback()

        if self._old_opacity:
            self._old_opacity.setOpacity(1.0)

        self.new_widget = self.stack.currentWidget()
        if self.new_widget and self._new_opacity:
            self._new_opacity.setOpacity(0.0)

        # Fade in
        self.fade_in = QPropertyAnimation(self._new_opacity, b"opacity", self)
        self.fade_in.setDuration(self.duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.finished.connect(self._on_fade_in_finished)

        self.fade_in.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        return effect

    def fade_both_stacks_in_parallel(
        self,
        right_stack: QStackedLayout,
        right_new_index: int,
        left_stack: QStackedLayout,
        left_new_index: int,
        width_ratio: tuple[float, float] = (0.5, 0.5),
    ):
        """
        Fades out both stacks in parallel, then in the 'finished' callback,
        we switch indexes, do any resizing, and fade them in.
        """
        old_right_idx = right_stack.currentIndex()
        old_left_idx = left_stack.currentIndex()
        if old_right_idx == right_new_index and old_left_idx == left_new_index:
            return

        self.old_right_widget = right_stack.widget(old_right_idx)
        self.old_left_widget = left_stack.widget(old_left_idx)
        self.new_right_widget = right_stack.widget(right_new_index)
        self.new_left_widget = left_stack.widget(left_new_index)

        if not self.old_right_widget or not self.old_left_widget:
            return

        self.fade_out_group = QParallelAnimationGroup(self)  # Keep a reference
        self.old_right_effect = self._ensure_opacity_effect(self.old_right_widget)
        self.old_left_effect = self._ensure_opacity_effect(self.old_left_widget)

        self.anim_out_right = QPropertyAnimation(
            self.old_right_effect, b"opacity", self
        )
        self.anim_out_right.setDuration(self.duration)
        self.anim_out_right.setStartValue(1.0)
        self.anim_out_right.setEndValue(0.0)
        self.anim_out_right.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_out_left = QPropertyAnimation(self.old_left_effect, b"opacity", self)
        self.anim_out_left.setDuration(self.duration)
        self.anim_out_left.setStartValue(1.0)
        self.anim_out_left.setEndValue(0.0)
        self.anim_out_left.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_out_group.addAnimation(self.anim_out_right)
        self.fade_out_group.addAnimation(self.anim_out_left)

        self.fade_out_group.finished.connect(
            lambda: self._switch_resize_and_fade_in_both(
                right_stack, right_new_index, left_stack, left_new_index, width_ratio
            )
        )

        self.fade_out_group.start()
        self._is_animating = True

    def _switch_resize_and_fade_in_both(
        self,
        right_stack: QStackedLayout,
        right_new_index: int,
        left_stack: QStackedLayout,
        left_new_index: int,
        width_ratio: tuple[float, float],
    ):
        right_stack.setCurrentIndex(right_new_index)
        left_stack.setCurrentIndex(left_new_index)

        self.old_right_effect.setOpacity(1.0)
        self.old_left_effect.setOpacity(1.0)

        self.new_right_widget.hide()
        self.new_left_widget.hide()
        nr_effect = self._ensure_opacity_effect(self.new_right_widget)
        nl_effect = self._ensure_opacity_effect(self.new_left_widget)
        nr_effect.setOpacity(0.0)
        nl_effect.setOpacity(0.0)

        total_width = self.main_widget.width()
        left_width = int(total_width * width_ratio[0])
        right_width = int(total_width * width_ratio[1])
        self.main_widget.left_stack.setMaximumWidth(left_width)
        self.main_widget.right_stack.setMaximumWidth(right_width)

        self._update_layout(self.main_widget)

        self.new_right_widget.show()
        self.new_left_widget.show()

        self.fade_in_group = QParallelAnimationGroup(self)
        anim_in_right = QPropertyAnimation(nr_effect, b"opacity", self)
        anim_in_right.setDuration(self.duration)
        anim_in_right.setStartValue(0.0)
        anim_in_right.setEndValue(1.0)
        anim_in_right.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_in_left = QPropertyAnimation(nl_effect, b"opacity", self)
        anim_in_left.setDuration(self.duration)
        anim_in_left.setStartValue(0.0)
        anim_in_left.setEndValue(1.0)
        anim_in_left.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.fade_in_group.addAnimation(anim_in_right)
        self.fade_in_group.addAnimation(anim_in_left)
        self.fade_in_group.finished.connect(self._on_fade_in_finished)
        self.fade_in_group.start()

    def _update_layout(self, widget: QWidget):
        layout = widget.layout()
        if layout:
            layout.invalidate()
            layout.activate()
        widget.resize(widget.size().width(), widget.size().height())

    @pyqtSlot()
    def _on_fade_in_finished(self):
        self._is_animating = False
        self._old_opacity = None
        self._new_opacity = None
        if self.new_widget:
            self.new_widget.setGraphicsEffect(None)
        if self.old_widget:
            self.old_widget.setGraphicsEffect(None)
        if self.new_left_widget:
            self.new_left_widget.setGraphicsEffect(None)
        if self.new_right_widget:
            self.new_right_widget.setGraphicsEffect(None)
        for i in range(self.stack.count()):
            widget = self.stack.widget(i)
            self.clear_graphics_effects(widget)

    def clear_graphics_effects(self, widget: QWidget) -> None:
        """Recursively clears GraphicsEffect from the given widget and its children."""
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)
        for child in widget.findChildren(QWidget):
            if child.__class__.__base__ == BaseIndicatorLabel:
                continue
            if child.graphicsEffect():
                child.setGraphicsEffect(None)
            # for child in widget.findChildren(QWidget):
            #     if child.graphicsEffect():
            #         child.setGraphicsEffect(None)
