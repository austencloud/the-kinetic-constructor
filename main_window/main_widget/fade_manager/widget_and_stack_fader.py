from typing import TYPE_CHECKING, Optional, List
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class WidgetAndStackFader:
    """Handles simultaneous fading of widgets and a stack."""

    def __init__(self, manager: "FadeManager"):
        self.manager = manager

    def fade_widgets_and_stack(
        self,
        widgets: List[QWidget],
        stack: QStackedWidget,
        new_index: int,
        duration: int = 300,
        callback: Optional[callable] = None,
    ):
        """Fades out widgets and stack in parallel, switches the stack, and fades both in."""
        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)

        if not current_widget or not next_widget or stack.currentIndex() == new_index:
            return

        # Clear any lingering graphics effects
        self.manager.graphics_effect_remover.clear_graphics_effects(
            [current_widget, next_widget] + widgets
        )

        # Prepare animations for widgets and stack
        animation_group = QParallelAnimationGroup(self.manager)

        # Fade out current widget
        if current_widget:
            self._add_fade_animation(
                animation_group, current_widget, fade_in=False, duration=duration
            )

        # Fade out widgets
        for widget in widgets:
            self._add_fade_animation(
                animation_group, widget, fade_in=False, duration=duration
            )

        def on_fade_out_finished():
            # Reset widgets and switch stack index
            if callback:
                callback()

            self.manager.graphics_effect_remover.clear_graphics_effects(
                [next_widget] + widgets
            )
            stack.setCurrentIndex(new_index)

            # Fade in new widget and widgets
            fade_in_group = QParallelAnimationGroup(self.manager)
            if next_widget:
                self._add_fade_animation(
                    fade_in_group, next_widget, fade_in=True, duration=duration
                )
            for widget in widgets:
                self._add_fade_animation(
                    fade_in_group, widget, fade_in=True, duration=duration
                )

            fade_in_group.start()

        # Connect animation group finished signal
        animation_group.finished.connect(on_fade_out_finished)

        # Start animations
        animation_group.start()

    def _add_fade_animation(
        self,
        group: QParallelAnimationGroup,
        widget: QWidget,
        fade_in: bool,
        duration: int,
    ):
        """Helper to add fade animations to a QParallelAnimationGroup."""
        effect = self.manager.widget_fader._ensure_opacity_effect(widget)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0 if fade_in else 1.0)
        animation.setEndValue(1.0 if fade_in else 0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        group.addAnimation(animation)
