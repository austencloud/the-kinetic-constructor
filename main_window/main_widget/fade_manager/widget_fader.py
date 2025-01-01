from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QStackedWidget
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager
    from main_window.main_widget.main_widget import MainWidget


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

        self.manager.clear_graphics_effects(widgets)

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
