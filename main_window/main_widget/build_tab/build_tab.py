# build_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSlot

from main_window.main_widget.build_tab.sequence_constructor import SequenceConstructor
from main_window.main_widget.build_tab.sequence_generator.sequence_generator import SequenceGenerator

from main_window.main_widget.build_tab.sequence_widget.sequence_widget import (
    SequenceWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BuildTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.layout:QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Initialize SequenceWidget (shared between Build and Generate)
        self.sequence_widget = SequenceWidget(self)

        # Initialize content stack for Build and Generate
        self.content_stack = QStackedWidget(self)
        self.sequence_constructor = SequenceConstructor(self)
        self.sequence_generator = SequenceGenerator(self)

        self.content_stack.addWidget(self.sequence_constructor)  # Index 0
        self.content_stack.addWidget(self.sequence_generator)   # Index 1

        # Apply opacity effect to the content stack for fade animations
        self.opacity_effect = QGraphicsOpacityEffect(self.content_stack)
        self.content_stack.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)  # Fully visible initially

        # Add widgets to the layout
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.content_stack)

    def show_build(self):
        """Display the Build (SequenceConstructor) content with fade animation."""
        if self.content_stack.currentWidget() == self.sequence_constructor:
            return  # Already showing
        self._fade_transition(to_index=0)

    def show_generate(self):
        """Display the Generate (SequenceGeneratorWidget) content with fade animation."""
        if self.content_stack.currentWidget() == self.sequence_generator:
            return  # Already showing
        self._fade_transition(to_index=1)

    def _fade_transition(self, to_index: int):
        """Handle fade-out and fade-in animations when switching between Build and Generate."""
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)  # Duration for fade-out and fade-in
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Fade-out
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(lambda: self._switch_content(to_index))
        self.animation.finished.connect(self._start_fade_in)
        self.animation.start()

    def _switch_content(self, to_index: int):
        """Switch the content after fade-out."""
        self.content_stack.setCurrentIndex(to_index)

    def _start_fade_in(self):
        """Start fade-in after switching content."""
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in.start()

    def paintEvent(self, event):
        """Handle custom painting if necessary."""
        painter = QPainter(self)
        painter.save()
        try:
            # Custom painting logic here (if needed)
            pass  # Replace with actual painting code if needed
        finally:
            painter.restore()
        # No need to call painter.end()
