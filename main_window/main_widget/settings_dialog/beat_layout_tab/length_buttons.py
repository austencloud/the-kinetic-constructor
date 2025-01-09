class LengthButton(QPushButton):
    """Button to increment or decrement the sequence length."""

    def __init__(self, parent: QWidget, text: str, callback):
        super().__init__(text, parent)
        self.clicked.connect(callback)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event):
        size = max(20, self.parent().width() // 40)
        self.setStyleSheet(f"font-size: {size}px;")
