# graph_editor_toggle_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class GraphEditorToggleTab(QWidget):
    """Toggle tab widget to expand/collapse the GraphEditor."""
    toggled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: gray; border-radius: 5px;")
        self.label = QLabel("Graph Editor", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.toggled.emit()
