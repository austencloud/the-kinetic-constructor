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
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex

logger = logging.getLogger(__name__)


class CodexAnimationManager(QObject):
    """Manages animations for the CodexWidget, including opening and closing."""

    ANIMATION_DURATION = 350  # milliseconds

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex

        # Initialize width animation
        self.width_animation = QPropertyAnimation(self.codex, b"maximumWidth")
        self.width_animation.setDuration(self.ANIMATION_DURATION)
        self.width_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Initialize geometry animation
        self.geometry_animation = QPropertyAnimation(self.codex, b"geometry")
        self.geometry_animation.setDuration(self.ANIMATION_DURATION)
        self.geometry_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Initialize opacity effect and animation
        self.opacity_effect = QGraphicsOpacityEffect(self.codex)
        self.codex.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(self.ANIMATION_DURATION)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Initialize placeholder animation if placeholder exists
        self.placeholder = getattr(codex.learn_widget, "placeholder", None)
        if self.placeholder:
            self.placeholder_animation = QPropertyAnimation(
                self.placeholder, b"minimumWidth"
            )
            self.placeholder_animation.setDuration(self.ANIMATION_DURATION)
            self.placeholder_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Group animations
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.width_animation)
        self.animation_group.addAnimation(self.geometry_animation)
        self.animation_group.addAnimation(self.opacity_animation)
        if self.placeholder:
            self.animation_group.addAnimation(self.placeholder_animation)

        # Track target width for determining state
        self.target_width = 0

        # Initially hide the Codex
        self.codex.setMaximumWidth(0)
        self.codex.hide()

    def toggle_codex(self, show: bool):
        """Toggle the visibility of the codex with animations for both showing and hiding."""
        logger.debug(f"Toggling codex visibility to {'show' if show else 'hide'}.")

        if self.animation_group.state() == QAbstractAnimation.State.Running:
            self.animation_group.stop()

        parent_widget = self.codex.parentWidget()
        parent_width = parent_widget.width()
        current_width = self.codex.maximumWidth()
        current_opacity = self.opacity_effect.opacity()

        if show:
            # Set target dimensions for showing
            self.codex.show()
            self.target_width = int(parent_width * 0.5)

            # Geometry animation
            self.geometry_animation.setStartValue(
                QRect(0, 0, current_width, self.codex.height())
            )
            self.geometry_animation.setEndValue(
                QRect(0, 0, self.target_width, self.codex.height())
            )

            # Width animation
            self.width_animation.setStartValue(current_width)
            self.width_animation.setEndValue(self.target_width)

            # Opacity animation
            self.opacity_animation.setStartValue(current_opacity)
            self.opacity_animation.setEndValue(1.0)

            # Placeholder animation
            if self.placeholder:
                self.placeholder_animation.setStartValue(0)
                self.placeholder_animation.setEndValue(self.target_width)

        else:
            # Set target dimensions for hiding
            self.target_width = 0

            # Geometry animation
            self.geometry_animation.setStartValue(
                QRect(0, 0, current_width, self.codex.height())
            )
            self.geometry_animation.setEndValue(
                QRect(0, 0, self.target_width, self.codex.height())
            )

            # Width animation
            self.width_animation.setStartValue(current_width)
            self.width_animation.setEndValue(self.target_width)

            # Opacity animation
            self.opacity_animation.setStartValue(current_opacity)
            self.opacity_animation.setEndValue(0.0)

            # Placeholder animation
            if self.placeholder:
                self.placeholder_animation.setStartValue(current_width)
                self.placeholder_animation.setEndValue(0)

        # Start animations
        self.animation_group.start()

    def on_animation_finished(self):
        """Handle post-animation actions."""
        if self.target_width == 0:
            self.codex.hide()
            self.opacity_effect.setOpacity(1.0)  # Reset opacity for future use
            logger.debug("Codex hidden after collapse animation.")
