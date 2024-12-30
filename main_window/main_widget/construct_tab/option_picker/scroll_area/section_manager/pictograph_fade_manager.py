# pictograph_fade_manager.py
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QObject,
    pyqtSignal,
    QParallelAnimationGroup,
    pyqtSlot,
)


class PictographFadeManager(QObject):
    """Manages fade-out/fade-in animations for pictograph containers."""
    
    fade_out_finished = pyqtSignal()
    fade_in_finished = pyqtSignal()

    def __init__(self, sections: list[QWidget], duration: int = 300):
        super().__init__()
        self.sections = sections  # List of pictograph_container widgets
        self.duration = duration
        self.is_animating = False
        self.fade_out_group = None
        self.fade_in_group = None

    def fade_out_pictographs(self):
        """Fade out all pictograph containers."""
        if self.is_animating:
            return
        self.fade_out_group = QParallelAnimationGroup(self)
        for section in self.sections:
            opacity_effect = self._ensure_opacity_effect(section)
            fade_out = QPropertyAnimation(opacity_effect, b"opacity")
            fade_out.setDuration(self.duration)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.fade_out_group.addAnimation(fade_out)
        self.fade_out_group.finished.connect(self.on_fade_out_finished)
        self.is_animating = True
        self.fade_out_group.start()

    @pyqtSlot()
    def on_fade_out_finished(self):
        """Called when fade-out completes."""
        self.fade_out_finished.emit()
        self.is_animating = False
        self.fade_out_group = None  # Reset for future animations

    def fade_in_pictographs(self):
        """Fade in all pictograph containers."""
        if self.is_animating:
            return
        self.fade_in_group = QParallelAnimationGroup(self)
        for section in self.sections:
            opacity_effect = self._ensure_opacity_effect(section)
            fade_in = QPropertyAnimation(opacity_effect, b"opacity")
            fade_in.setDuration(self.duration)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.fade_in_group.addAnimation(fade_in)
        self.fade_in_group.finished.connect(self.on_fade_in_finished)
        self.is_animating = True
        self.fade_in_group.start()

    @pyqtSlot()
    def on_fade_in_finished(self):
        """Called when fade-in completes."""
        self.fade_in_finished.emit()
        self.is_animating = False
        self.fade_in_group = None  # Reset for future animations

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Ensure the widget has a QGraphicsOpacityEffect."""
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect
