from typing import TYPE_CHECKING, Optional, Union
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class WidgetFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager

    def fade_widgets(
        self,
        widgets: list[QWidget],
        fade_in: bool,
        duration: int,
        callback: Optional[callable] = None,
    ) -> None:
        if not widgets:
            if callback:
                callback()
            return

        self.manager.graphics_effect_remover.clear_graphics_effects(widgets)

        animation_group = QParallelAnimationGroup(self.manager)
        for widget in widgets:
            effect = self._ensure_opacity_effect(widget)
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0 if fade_in else 1.0)
            animation.setEndValue(1.0 if fade_in else 0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(animation)
        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect

    def fade_and_update(
        self,
        widget: list[QWidget],
        callback: Union[callable, tuple[callable, callable]] = None,
        duration: int = 250,
    ) -> None:
        def on_fade_out_finished():
            self.manager.graphics_effect_remover.clear_graphics_effects(widget)

            if callback:
                if isinstance(callback, tuple):
                    # Execute the first callback
                    callback[0]()
                    # Fade widgets back in and execute the second callback after fade-in
                    self.fade_widgets(
                        widget, True, duration, lambda: callback[1]()
                    )
                else:
                    # Execute single callback before fading back in
                    callback()
                    self.fade_widgets(widget, True, duration)

        # Start fading out the widgets and connect the fade-out animation to the callback
        self.fade_widgets(widget, False, duration, on_fade_out_finished)