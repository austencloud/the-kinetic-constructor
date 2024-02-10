from PyQt6.QtWidgets import QWidget, QHBoxLayout

from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)


class SectionGroupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)  # Adjust spacing as needed
        self.setLayout(self.layout)

    def add_section_widget(self, section: SectionWidget):
        self.layout.addWidget(section)
