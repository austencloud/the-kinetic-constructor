# pictograph_fade_manager.py
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication
from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QObject,
    pyqtSignal,
    QParallelAnimationGroup,
    pyqtSlot,
)
from typing import TYPE_CHECKING

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )
    from main_window.main_widget.learn_tab.learn_tab import LearnTab


class LessonWidgetFadeManager(QObject):
    """Manages fade-out/fade-in animations for pictograph containers."""

    def __init__(self, lesson_widget: "BaseLessonWidget") -> None:
        super().__init__(lesson_widget)
        self.learn_tab = lesson_widget.learn_tab
        self.lesson = lesson_widget
        self.fade_out_group = None
        self.fade_in_group = None

    def fade_and_update_lesson(self):
        self.fade_out_group = QParallelAnimationGroup(self)
        group = self.get_widgets()

        for widget in group:
            animation = self.fade_out(widget)
            self.fade_out_group.addAnimation(animation)

        self.fade_out_group.finished.connect(self.on_fade_out_finished)
        self.fade_out_group.start()

    def get_widgets(self) -> list["QWidget"]:
        group = []
        group.append(self.lesson.answers_widget)
        letter_label = self.lesson.question_widget.letter_label
        pictograph = self.lesson.question_widget.pictograph
        if letter_label:
            group.append(letter_label)
        if pictograph:
            group.append(pictograph.view)
        return group

    def fade_out(self, widget: "QWidget", duration: int = 200) -> QPropertyAnimation:
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    def fade_in(self, widget: "QWidget", duration: int = 200) -> QPropertyAnimation:
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    @pyqtSlot()
    def on_fade_out_finished(self):
        """Called after all fade-out animations finish. Update pictographs and start fade-in."""
        self.lesson.clear_current_question()
        self.lesson.question_generator.generate_question()
        # QApplication.processEvents()

        widgets = self.get_widgets()
        self.fade_in_group = QParallelAnimationGroup(self)

        for section in widgets:
            animation = self.fade_in(section)
            self.fade_in_group.addAnimation(animation)

        self.fade_in_group.start()
        self.fade_in_group.finished.connect(self._on_fade_in_finished)

    @pyqtSlot()
    def _on_fade_in_finished(self):
        for widget in self.get_widgets():
            self.clear_graphics_effects(widget)

    def clear_graphics_effects(self, widget: QWidget) -> None:
        """Recursively clears GraphicsEffect from the given widget and its children."""
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)
        for child in widget.findChildren(QWidget):
            if child.__class__.__base__ == BaseIndicatorLabel:
                continue
            if child.graphicsEffect():
                child.setGraphicsEffect(None)
            # for child in widget.findChildren(QWidget):
            #     if child.__class__.__base__ == BaseIndicatorLabel:
            #         continue
            #     if child.graphicsEffect():
            #         child.setGraphicsEffect(None)
