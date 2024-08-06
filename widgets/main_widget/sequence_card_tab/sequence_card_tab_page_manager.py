from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab
    from widgets.main_widget.main_widget import MainWidget


class SequenceCardTabPageFactory:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def create_pages(self, num_pages: int) -> list[QGridLayout]:
        pages = []
        for _ in range(num_pages):
            page_row_layout = QHBoxLayout()
            page_row_layout.setSpacing(self.sequence_card_tab.margin)
            page_row_layout.setContentsMargins(
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
            )
            self.sequence_card_tab.scroll_layout.addLayout(page_row_layout)
            for _ in range(2):  # Two pages per row
                page_frame = QFrame(self.sequence_card_tab.scroll_content)
                page_frame.setFixedSize(
                    self.sequence_card_tab.page_width,
                    self.sequence_card_tab.page_height,
                )
                page_frame.setStyleSheet(
                    "background-color: white; border: 1px solid black;"
                )
                page_layout = QGridLayout(page_frame)
                page_layout.setContentsMargins(0, 0, 0, 0)
                page_layout.setSpacing(0)
                page_row_layout.addWidget(page_frame)
                pages.append(page_layout)
        return pages
