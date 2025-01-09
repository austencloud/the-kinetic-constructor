class LayoutDropdown(QComboBox):
    """Dropdown for selecting layouts."""

    def __init__(self, parent: QWidget, valid_layouts):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.addItems([f"{rows} x {cols}" for rows, cols in valid_layouts])

    def resizeEvent(self, event):
        font_size = max(10, self.parent().width() // 50)
        self.setStyleSheet(f"font-size: {font_size}px;")
