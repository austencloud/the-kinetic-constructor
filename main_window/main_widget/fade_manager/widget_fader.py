from typing import TYPE_CHECKING, Optional, Union
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QGraphicsItem
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from base_widgets.base_pictograph.glyphs.tka.tka_glyph import TKA_Glyph

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
                    callback[0]()
                    self.fade_widgets(
                        widget,
                        True,
                        duration,
                        lambda: QTimer.singleShot(0, callback[1]),
                    )
                else:
                    callback()
                    self.fade_widgets(widget, True, duration)

        self.fade_widgets(widget, False, duration, on_fade_out_finished)

    def fade_widgets_to_opacity(
        self,
        widgets: list,
        opacity: float,
        duration: int = 300,
        callback: Optional[callable] = None,
    ) -> None:
        if not widgets:
            if callback:
                callback()
            return
        if len(widgets) == 1 and isinstance(widgets[0], TKA_Glyph):
            widgets = widgets[0].childItems()

        self.manager.graphics_effect_remover.clear_graphics_effects(widgets)

        animation_group = QParallelAnimationGroup(self.manager)
        for widget in widgets:
            if isinstance(widget, QGraphicsItem):
                # Directly set opacity for QGraphicsItem
                widget.setOpacity(opacity)
            elif isinstance(widget, QWidget):
                effect = self._ensure_opacity_effect(widget)
                if effect:
                    start_opacity = effect.opacity() if effect else 1.0
                    animation = QPropertyAnimation(effect, b"opacity")
                    animation.setDuration(duration)
                    animation.setStartValue(start_opacity)
                    animation.setEndValue(opacity)
                    animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                    animation_group.addAnimation(animation)
        if callback:
            animation_group.finished.connect(callback)
        animation_group.start()
