from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
)
from PyQt6.QtWidgets import QHBoxLayout

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class MainWidgetLayoutManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def configure_layouts(self) -> None:
        left_frame = self._setup_left_frame()
        right_frame = self._setup_right_frame()
        self._setup_main_layout(left_frame, right_frame)

    def _setup_main_layout(self, left_frame, right_frame) -> None:
        self.main_widget.layout: QHBoxLayout = QHBoxLayout(self.main_widget)
        self.main_widget.layout.addWidget(left_frame)
        self.main_widget.layout.addWidget(right_frame)

    def _setup_right_frame(self) -> QFrame:
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.addWidget(self.main_widget.main_tab_widget)
        return right_frame

    def _setup_left_frame(self) -> QFrame:
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        left_layout.addWidget(self.main_widget.main_sequence_widget)
        return left_frame
