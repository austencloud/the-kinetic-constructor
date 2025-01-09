from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import Qt


if TYPE_CHECKING:

    from .option_scroll import OptionScroll


class OptionScrollLayoutManager:
    """ Manages the layout of the OptionScroll. """

    def __init__(self, option_scroll: "OptionScroll") -> None:
        self.option_scroll = option_scroll
        self._setup_layout()

    def _setup_layout(self):
        self.option_scroll.setWidgetResizable(True)
        self.option_scroll.setContentsMargins(0, 0, 0, 0)
        self.option_scroll.setStyleSheet("background-color: transparent; border: none;")

        self.option_scroll.layout = QVBoxLayout()
        self.option_scroll.layout.setContentsMargins(0, 0, 0, 0)
        self.option_scroll.layout.setSpacing(0)
        self.option_scroll.layout.setContentsMargins(0, 0, 0, 0)

        self.option_scroll.container = QWidget()
        self.option_scroll.container.setAutoFillBackground(True)
        self.option_scroll.container.setStyleSheet("background: transparent;")
        self.option_scroll.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.option_scroll.container.setLayout(self.option_scroll.layout)
        self.option_scroll.setWidget(self.option_scroll.container)

        self.option_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.option_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.option_scroll.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.option_scroll.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

