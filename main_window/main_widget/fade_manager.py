# unified_fade_manager.py

from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    pyqtSlot,
    QParallelAnimationGroup,
)
from PyQt6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class FadeManager(QObject):
    """Manages synchronized fade-out and fade-in animations for main and build widgets."""

    duration: int = 350

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_stacked_widget = main_widget.main_stacked_widget
        self.build_stacked_widget = main_widget.build_tab.build_stacked_widget

        # Initialize opacity effects
        self.main_opacity_effect = QGraphicsOpacityEffect(self.main_stacked_widget)
        self.main_stacked_widget.setGraphicsEffect(self.main_opacity_effect)
        self.main_opacity_effect.setOpacity(1.0)

        self.build_opacity_effect = QGraphicsOpacityEffect(self.build_stacked_widget)
        self.build_stacked_widget.setGraphicsEffect(self.build_opacity_effect)
        self.build_opacity_effect.setOpacity(1.0)

        self._is_animating = False

    def fade_to_tabs(
        self,
        new_main_index: int,
        new_build_index: Optional[int] = None,
        on_finished: Optional[Callable] = None,
    ) -> None:
        """Fades out the current main and build tabs and fades in the new ones."""
        if self._is_animating:
            return

        self._is_animating = True

        animation_group = QParallelAnimationGroup(self)

        # Fade-out main
        fade_out_main = QPropertyAnimation(self.main_opacity_effect, b"opacity")
        fade_out_main.setDuration(self.duration)
        fade_out_main.setStartValue(1.0)
        fade_out_main.setEndValue(0.0)
        fade_out_main.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation_group.addAnimation(fade_out_main)

        # Fade-out build if applicable
        if new_build_index is not None:
            fade_out_build = QPropertyAnimation(self.build_opacity_effect, b"opacity")
            fade_out_build.setDuration(self.duration)
            fade_out_build.setStartValue(1.0)
            fade_out_build.setEndValue(0.0)
            fade_out_build.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(fade_out_build)

        # Connect the end of fade-out to switch tabs
        animation_group.finished.connect(
            lambda: self._switch_tabs(new_main_index, new_build_index, on_finished)
        )

        animation_group.start()

    def _switch_tabs(
        self,
        new_main_index: int,
        new_build_index: Optional[int],
        on_finished: Optional[Callable],
    ) -> None:
        """Switches the main and build tabs and starts fade-in animations."""
        self.main_stacked_widget.setCurrentIndex(new_main_index)
        if new_build_index is not None:
            self.build_stacked_widget.setCurrentIndex(new_build_index)

        # Start fade-in animations
        animation_group = QParallelAnimationGroup(self)

        fade_in_main = QPropertyAnimation(self.main_opacity_effect, b"opacity")
        fade_in_main.setDuration(self.duration)
        fade_in_main.setStartValue(0.0)
        fade_in_main.setEndValue(1.0)
        fade_in_main.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation_group.addAnimation(fade_in_main)

        if new_build_index is not None:
            fade_in_build = QPropertyAnimation(self.build_opacity_effect, b"opacity")
            fade_in_build.setDuration(self.duration)
            fade_in_build.setStartValue(0.0)
            fade_in_build.setEndValue(1.0)
            fade_in_build.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation_group.addAnimation(fade_in_build)

        if on_finished:
            animation_group.finished.connect(on_finished)

        animation_group.finished.connect(self._animation_finished)
        animation_group.start()

    @pyqtSlot()
    def _animation_finished(self) -> None:
        """Resets the animation flag after completion."""
        self._is_animating = False
