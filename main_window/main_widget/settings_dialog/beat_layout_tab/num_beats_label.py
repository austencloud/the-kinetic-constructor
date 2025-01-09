class NumBeatsLabel(QLabel):
    """Label displaying the current number of beats."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_label(self, num_beats: int):
        self.setText(str(num_beats))

    def resizeEvent(self, event):
        size = max(20, self.parent().width() // 40)
        self.setStyleSheet(f"font-size: {size}px;")
