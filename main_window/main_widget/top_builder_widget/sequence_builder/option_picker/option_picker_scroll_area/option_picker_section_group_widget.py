from PyQt6.QtWidgets import QWidget, QHBoxLayout


class OptionPickerSectionGroupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)  # Adjust spacing as needed
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def add_section_widget(self, section):
        self.layout.addWidget(section)
