from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsOpacityEffect,
    QStackedWidget,
)
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    pyqtSlot,
)

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class FadeManager(QObject):
    """
    A centralized manager for handling fade-out/fade-in animations across the application.
    """

    left_old_widget: Optional[QWidget] = None
    left_new_widget: Optional[QWidget] = None
    right_old_widget: Optional[QWidget] = None
    right_new_widget: Optional[QWidget] = None
    widgets_to_fade_out: Optional[list[QWidget]] = []
    widgets_to_fade_in: Optional[list[QWidget]] = []
    default_duration = 250

    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self._is_animating = False

    def fade_widgets(
        self,
        fade_in: bool,
        callback: Optional[callable] = None,
    ):
        """
        Fades a list of widgets either in or out.
        """
        if fade_in:
            widgets_to_fade = self.widgets_to_fade_in
        elif not fade_in:
            widgets_to_fade = self.widgets_to_fade_out
            if not self.widgets_to_fade_out:
                if callback:
                    callback()
                return

        animation_group = QParallelAnimationGroup(self)
        self.clear_graphics_effects()
        for widget in widgets_to_fade:
            effect = self._ensure_opacity_effect(widget)
            animation = QPropertyAnimation(effect, b"opacity", self)
            animation.setDuration(self.default_duration)
            animation.setStartValue(0.0 if fade_in else 1.0)
            animation.setEndValue(1.0 if fade_in else 0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(animation)

        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def fade_stack(
        self,
        stack: QStackedWidget,
        new_index: int,
        callback: Optional[callable] = None,
    ):
        """
        Fades out the current widget in a stack, switches to a new index, and fades in the new widget.
        """
        self.stack = stack
        if self._is_animating or stack.currentIndex() == new_index:
            return

        self._is_animating = True
        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)

        if not current_widget or not next_widget:
            return

        self.widgets_to_fade_out = [current_widget]
        self.widgets_to_fade_in = [next_widget]

        self.fade_widgets(
            fade_in=False,
            callback=lambda: self._on_stack_fade_out(stack, new_index, callback),
        )

    def _on_stack_fade_out(
        self,
        stack: QStackedWidget,
        new_index: int,
        callback: Optional[callable],
    ) -> None:
        stack.setCurrentIndex(new_index)
        self.clear_graphics_effects()
        self.fade_widgets(True, lambda: self._on_stack_fade_in(callback))

    def _on_stack_fade_in(self, callback: Optional[callable]):
        self._is_animating = False
        if callback:
            callback()

    def fade_and_update(
        self, widgets_to_fade: list[QWidget], update_callback: callable
    ) -> None:
        self.widgets_to_fade_out = widgets_to_fade
        self.fade_widgets(
            False,
            callback=lambda: self._on_update_fade_out(update_callback),
        )

    def _on_update_fade_out(self, update_callback: callable):
        update_callback()
        self.fade_widgets(fade_in=True)

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect

    def fade_both_stacks_in_parallel(
        self,
        right_stack: QStackedWidget,
        right_new_index: int,
        left_stack: QStackedWidget,
        left_new_index: int,
        width_ratio: tuple[float, float],
    ):
        if self._is_animating:
            return

        self._is_animating = True
        self.clear_graphics_effects()

        self.right_old_widget = right_stack.currentWidget()
        self.left_old_widget = left_stack.currentWidget()

        self.right_new_widget = right_stack.widget(right_new_index)
        self.left_new_widget = left_stack.widget(left_new_index)

        if not (
            self.right_old_widget
            and self.left_old_widget
            and self.right_new_widget
            and self.left_new_widget
        ):
            self._is_animating = False
            return

        self.clear_graphics_effects()

        # Fade out current widgets
        animations = []
        animations.append(
            self.create_fade_animation(self.right_old_widget, fade_in=False)
        )
        animations.append(
            self.create_fade_animation(self.left_old_widget, fade_in=False)
        )

        # Adjust layout width after fade-out
        def switch_and_resize():
            right_stack.setCurrentIndex(right_new_index)
            left_stack.setCurrentIndex(left_new_index)

            total_width = self.main_widget.width()
            left_width = int(total_width * width_ratio[0])
            right_width = int(total_width * width_ratio[1])

            left_stack.setMinimumWidth(left_width)
            # right_stack.setMaximumWidth(right_width)
            # self._update_layout(self.main_widget)

        # Fade in new widgets
        def fade_in_new_widgets():
            animations = [
                self.create_fade_animation(self.right_new_widget, fade_in=True),
                self.create_fade_animation(self.left_new_widget, fade_in=True),
            ]
            fade_in_group = QParallelAnimationGroup(self)
            for anim in animations:
                fade_in_group.addAnimation(anim)
            fade_in_group.finished.connect(self._on_fade_in_finished)
            fade_in_group.start()

        fade_out_group = QParallelAnimationGroup(self)
        for anim in animations:
            fade_out_group.addAnimation(anim)
        fade_out_group.finished.connect(
            lambda: (switch_and_resize(), fade_in_new_widgets())
        )
        fade_out_group.start()

    def create_fade_animation(
        self, widget: QWidget, fade_in: bool
    ) -> QPropertyAnimation:
        effect = self._ensure_opacity_effect(widget)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(self.default_duration)
        animation.setStartValue(0.0 if fade_in else 1.0)
        animation.setEndValue(1.0 if fade_in else 0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect

    def _on_fade_in_finished(self):
        self._is_animating = False
        self._old_opacity = None
        self._new_opacity = None

        for i in range(self.stack.count()):
            self.clear_graphics_effects()

    def clear_graphics_effects(self) -> None:
        """Recursively clears GraphicsEffect from the given widget and its children."""
        widgets = (
            [
                self.right_old_widget,
                self.left_old_widget,
                self.right_new_widget,
                self.left_new_widget,
            ]
            + self.widgets_to_fade_out
            + self.widgets_to_fade_in
        )

        for widget in widgets:
            if widget:
                widget.setGraphicsEffect(None)
                for child in widget.findChildren(QWidget):
                    if not isinstance(child, BaseIndicatorLabel):
                        child.setGraphicsEffect(None)

    def _update_layout(self, widget: QWidget):
        layout = widget.layout()
        if layout:
            layout.invalidate()
            layout.activate()
        widget.resize(widget.size().width(), widget.size().height())
