from typing import TYPE_CHECKING
from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QParallelAnimationGroup,
    pyqtProperty,
    QObject,
)
from PyQt6.QtGui import QColor

if TYPE_CHECKING:
    from .letter_type_widget import LetterTypeButton


class LetterTypeButtonAnimator(QObject):
    def __init__(self, button_widget: "LetterTypeButton"):
        super().__init__(button_widget)
        self._scale = 1.0
        self._bg_color = QColor("white")
        self.press_scale = 0.9
        self.press_anim_duration = 120
        self.color_anim_duration = 300
        self.button_widget = button_widget
        self.anim_group = QParallelAnimationGroup(self)

        self.scale_anim = QPropertyAnimation(self, b"clickScale")
        self.scale_anim.setDuration(self.press_anim_duration)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim_group.addAnimation(self.scale_anim)

        self.color_anim = QPropertyAnimation(self, b"backgroundColor")
        self.color_anim.setDuration(self.color_anim_duration)
        self.color_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim_group.addAnimation(self.color_anim)

    @pyqtProperty(float)
    def clickScale(self):
        return self._scale

    @clickScale.setter
    def clickScale(self, value):
        self._scale = value
        self.button_widget.update()

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._bg_color

    @backgroundColor.setter
    def backgroundColor(self, value: QColor):
        self._bg_color = value
        self.button_widget.updater.update_stylesheet()

    def animate_hover(self, entering: bool, base_color: QColor):
        self.color_anim.stop()
        self.color_anim.setStartValue(self._bg_color)

        if entering:
            end_col = QColor("lightgray")
        else:
            end_col = base_color

        self.color_anim.setEndValue(end_col)
        self.anim_group.setCurrentTime(0)
        self.anim_group.start()

    def animate_press(self):
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(self.press_scale)
        self.anim_group.start()

    def animate_release(self):
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(1.0)
        self.anim_group.start()
