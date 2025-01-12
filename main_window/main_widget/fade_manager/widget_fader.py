import os
from typing import TYPE_CHECKING, Optional, Union
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QGraphicsItem
from PyQt6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)
from Enums.Enums import Glyph
from base_widgets.base_pictograph.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class WidgetFader:
    def __init__(self, manager: "FadeManager"):
        self.manager = manager
        self.profiler = manager.main_widget.main_window.profiler

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

        # self.profiler.enable()


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

        # self.profiler.disable()
        # self.profiler.write_profiling_stats_to_file(
        #     "option_updater_profile.txt", os.getcwd()
        # )


    def fade_visibility_items_to_opacity(
        self,
        visibility_element: Union[Glyph, NonRadialPointsGroup],
        opacity: float,
        duration: int = 300,
        callback: Optional[callable] = None,
    ) -> None:
        if not visibility_element:
            if callback:
                callback()
            return
        items = self._get_corresponding_items(visibility_element)

        self.manager.graphics_effect_remover.clear_graphics_effects(
            [visibility_element]
        )
        animation_group = QParallelAnimationGroup(self.manager)
        for item in items:
            self.manager.graphics_effect_remover.clear_graphics_effects([item])
            if isinstance(item, QGraphicsItem):
                item.setOpacity(opacity)
            elif isinstance(item, QWidget):
                effect = self._ensure_opacity_effect(item)
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

    def _get_corresponding_items(
        self, element: Union[Glyph, NonRadialPointsGroup]
    ) -> list[Union[Glyph, NonRadialPointsGroup]]:
        if element.name == "TKA":
            items = element.get_all_items()
        elif element.name == "VTG":
            items = [element]
        elif element.name == "Elemental":
            items = [element]
        elif element.name == "Positions":
            items = element.get_all_items()
        elif element.name == "Reversals":
            items = list(element.reversal_items.values())
        elif element.name == "non_radial_points":
            items = element.child_points
        return items

