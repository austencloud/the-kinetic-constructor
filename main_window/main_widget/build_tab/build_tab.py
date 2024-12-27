# build_tab.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

from main_window.main_widget.build_tab.sequence_constructor import SequenceConstructor

from .sequence_generator.sequence_generator import SequenceGenerator
from .sequence_widget.sequence_widget import SequenceWidget


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BuildTab(QWidget):
    """
    Manages SequenceConstructor and Generator.
    """

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.sequence_widget = SequenceWidget(self)
        self.build_stacked_widget = QStackedWidget(self)
        self.sequence_constructor = SequenceConstructor(self)
        self.sequence_generator = SequenceGenerator(self)

        self.build_stacked_widget.addWidget(self.sequence_constructor)
        self.build_stacked_widget.addWidget(self.sequence_generator)
        self.layout.addWidget(self.sequence_widget, 1)
        self.layout.addWidget(self.build_stacked_widget, 1)
