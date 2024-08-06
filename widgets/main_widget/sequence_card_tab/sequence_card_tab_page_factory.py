from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab

class SequenceCardTabPageFactory:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.current_row_layout = None  # Track the current row layout

    def create_page(self) -> QGridLayout:
        # Check if we need to start a new row
        if self.current_row_layout is None or self.current_row_layout.count() >= 2:
            self.current_row_layout = QHBoxLayout()
            self.current_row_layout.setSpacing(self.sequence_card_tab.margin)
            self.current_row_layout.setContentsMargins(
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
            )
            self.sequence_card_tab.scroll_layout.addLayout(self.current_row_layout)

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
        self.current_row_layout.addWidget(page_frame)

        return page_layout
