# build_tab.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

from main_window.main_widget.build_tab.build_tab_fade_manager import BuildTabFadeManager
from main_window.main_widget.build_tab.sequence_constructor import SequenceConstructor

from .sequence_generator.sequence_generator import SequenceGenerator
from .sequence_widget.sequence_widget import SequenceWidget


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BuildTab(QWidget):
    """
    Unified BuildTab managing SequenceConstructor and SequenceGeneratorWidget.
    Utilizes BuildTabFadeManager for internal transitions to ensure consistent fade animations.
    """

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Initialize Layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Initialize SequenceWidget (shared across all primary tabs)
        self.sequence_widget = SequenceWidget(self)

        # Initialize content stack for SequenceConstructor and SequenceGeneratorWidget
        self.build_stacked_widget = QStackedWidget(self)
        self.sequence_constructor = SequenceConstructor(self)
        self.sequence_generator = SequenceGenerator(self)

        self.build_stacked_widget.addWidget(self.sequence_constructor)
        self.build_stacked_widget.addWidget(self.sequence_generator)

        # Initialize BuildTabFadeManager for internal tabs

        # Add widgets to the layout
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.build_stacked_widget)

    def show_construct(self) -> None:
        """
        Display the SequenceConstructor content with fade animation.
        """
        if self.build_stacked_widget.currentWidget() == self.sequence_constructor:
            return

    def show_generate(self) -> None:
        """
        Display the SequenceGeneratorWidget content with fade animation.
        """
        if self.build_stacked_widget.currentWidget() == self.sequence_generator:
            return
