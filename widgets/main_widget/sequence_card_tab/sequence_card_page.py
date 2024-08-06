from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt


class SequenceCardPage(QWidget):
    def __init__(self, parent_tab, page_width: int, page_height: int, margin: int):
        super().__init__()
        self.parent_tab = parent_tab
        self.page_width = page_width
        self.page_height = page_height
        self.margin = margin
        self.setFixedSize(page_width, page_height)
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
    def add_image(self, label, row: int, col: int):
        self.layout.addWidget(label, row, col)
