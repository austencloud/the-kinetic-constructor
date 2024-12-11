# codex_animation_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
import logging

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex

logger = logging.getLogger(__name__)


class CodexAnimationManager:
    """Manages animations for the CodexWidget."""

    def __init__(self, parent: "Codex"):
        self.parent = parent
        self.setup_animation()

    def setup_animation(self):
        self.parent.animation = QPropertyAnimation(self.parent, b"maximumWidth")
        self.parent.animation.setDuration(300)
        self.parent.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def toggle_codex(self, show: bool):
        logger.debug(f"Toggling codex visibility to {'show' if show else 'hide'}.")
        end_val = int(self.parent.learn_widget.width() * 0.5) if show else 0
        self.parent.animation.stop()
        self.parent.animation.setStartValue(self.parent.width())
        self.parent.animation.setEndValue(end_val)
        self.parent.animation.finished.connect(lambda: self.parent.setFixedWidth(end_val))
        self.parent.animation.start()
