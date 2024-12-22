from typing import TYPE_CHECKING
from PyQt6.QtCore import (
    QPropertyAnimation,
    QRect,
    QEasingCurve,
    QObject,
    QAbstractAnimation,
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QParallelAnimationGroup
import logging

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex.codex import Codex

logger = logging.getLogger(__name__)


class CodexAnimationManager(QObject):
    """Manages animations for the CodexWidget, including opening and closing."""

    ANIMATION_DURATION = 350  # milliseconds

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex


        self.opacity_effect = QGraphicsOpacityEffect(self.codex)
        self.codex.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(self.ANIMATION_DURATION)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.placeholder = getattr(codex.learn_widget, "placeholder", None)
        if self.placeholder:
            self.placeholder_animation = QPropertyAnimation(
                self.placeholder, b"minimumWidth"
            )
            self.placeholder_animation.setDuration(self.ANIMATION_DURATION)
            self.placeholder_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.opacity_animation)
        if self.placeholder:
            self.animation_group.addAnimation(self.placeholder_animation)

        self.target_width = 0

    def animate(self, show: bool):
        """Toggle the visibility of the codex with animations for both showing and hiding."""
        logger.debug(f"Toggling codex visibility to {'show' if show else 'hide'}.")

        if self.animation_group.state() == QAbstractAnimation.State.Running:
            self.animation_group.stop()

        parent_widget = self.codex.parentWidget()
        parent_width = parent_widget.width()
        current_opacity = self.opacity_effect.opacity()

        if show:
            self.codex.show()
            self.target_width = int(parent_width * 0.5)
            self.opacity_animation.setStartValue(current_opacity)
            self.opacity_animation.setEndValue(1.0)

        else:
            self.target_width = 0
            self.opacity_animation.setStartValue(current_opacity)
            self.opacity_animation.setEndValue(0.0)

        self.animation_group.start()

    def on_animation_finished(self):
        """Handle post-animation actions."""
        if self.target_width == 0:
            self.codex.hide()
            self.opacity_effect.setOpacity(1.0)
            logger.debug("Codex hidden after collapse animation.")
