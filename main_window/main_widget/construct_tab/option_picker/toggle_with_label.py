from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from pytoggle import PyToggle

class ToggleWithLabel(QWidget):
    def __init__(self, label_text: str, parent=None):
        super().__init__(parent)
        self.layout:QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.label = QLabel(label_text)
        self.toggle = PyToggle(
            width=60,
            bg_color="#777",           # Gray when unchecked
            active_color="#00BCff",    # Blue when checked
            circle_color="#DDD",
            change_bg_on_state=True    # Enable background color change
        )
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.toggle)
