from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab

class SequenceCardTabPageFactory:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def create_page(self) -> QGridLayout:
        # Start a new row layout if necessary (only two pages per row)
        if not self.sequence_card_tab.scroll_layout.count() or \
           self.sequence_card_tab.scroll_layout.itemAt(self.sequence_card_tab.scroll_layout.count() - 1).layout().count() >= 2:
            current_row_layout = QHBoxLayout()
            current_row_layout.setSpacing(self.sequence_card_tab.margin)
            current_row_layout.setContentsMargins(
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
                self.sequence_card_tab.margin,
            )
            self.sequence_card_tab.scroll_layout.addLayout(current_row_layout)
        else:
            current_row_layout = self.sequence_card_tab.scroll_layout.itemAt(self.sequence_card_tab.scroll_layout.count() - 1).layout()

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
        current_row_layout.addWidget(page_frame)

        return page_layout
