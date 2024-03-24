from PyQt6.QtWidgets import QWidget, QHBoxLayout

from widgets.scroll_area.components.section_manager.section_widget.letterbook_section_widget import (
    LetterBookSectionWidget,
)


class SectionGroupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)  # Adjust spacing as needed
        self.setLayout(self.layout)

    def add_section_widget(self, section: LetterBookSectionWidget):
        self.layout.addWidget(section)
