from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QStackedLayout

from PyQt6.QtCore import (
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    pyqtSlot,
    QObject,
)

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionPickerFadeManager(QObject):
    duration: int = 200

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker = option_picker
        self._old_opacity: Optional[QGraphicsOpacityEffect] = None
        self._new_opacity: Optional[QGraphicsOpacityEffect] = None
        self._is_animating = False

    def fade_option_picker(
        self, option_picker: "OptionPicker", next_options: list[dict]
    ):

        self._old_opacity = self._ensure_opacity_effect(option_picker)
        self.fade_out = QPropertyAnimation(self._old_opacity, b"opacity", self)
        self.fade_out.setDuration(self.duration)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out.finished.connect(
            lambda: self._update_and_fade_in_option_picker(option_picker, next_options)
        )
        self.fade_out.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _update_and_fade_in_option_picker(
        self, option_picker: "OptionPicker", next_options: list[dict]
    ):

        # option_picker.scroll_area.clear_pictographs()
        # option_picker.scroll_area.add_and_display_relevant_pictographs(next_options)
        
        
        self._new_opacity = self._ensure_opacity_effect(option_picker)
        self.fade_in = QPropertyAnimation(self._new_opacity, b"opacity", self)
        self.fade_in.setDuration(self.duration)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.finished.connect(self._on_fade_in_finished)
        self.fade_in.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        return effect

    @pyqtSlot()
    def _on_fade_in_finished(self):
        self._is_animating = False
