from PyQt6.QtWidgets import QLabel, QTextEdit, QWidget, QStackedLayout
from PyQt6.QtCore import Qt, QEvent

class EditableLabel(QWidget):
    def __init__(self, parent, label_text: str, align=Qt.AlignmentFlag.AlignLeft, padding=5, bg_color="#FFFFFF"):
        super().__init__(parent)
        self.label = QLabel(label_text, self)
        self.edit = QTextEdit(self)  # Use QTextEdit for multi-line text
        self._align = align
        self._padding = padding
        self._bg_color = bg_color

        # Configure layout for stacked editing
        self.layout:QStackedLayout = QStackedLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

        # Apply initial styles and alignment
        self.apply_styles()
        self.setLayout(self.layout)
        self.label.mousePressEvent = self._show_edit  # Edit on click

        # Install event filter on QTextEdit to detect Enter key
        self.edit.installEventFilter(self)

    def eventFilter(self, source, event):
        """Detect Enter key press in QTextEdit to exit edit mode."""
        if source == self.edit and event.type() == QEvent.KeyPress and event.key() == Qt.Key.Key_Return:
            self._hide_edit()
            return True
        return super().eventFilter(source, event)

    def apply_styles(self):
        """Applies alignment, padding, and color styling to label and edit fields."""
        self.label.setAlignment(self._align)
        self.edit.setAlignment(self._align)
        self.label.setStyleSheet(f"padding: 0px; margin: 0px;")
        self.edit.setStyleSheet(
            f"background-color: {self._bg_color}; padding: {self._padding}px; margin: 0px;"
        )

    def _show_edit(self, event=None):
        """Switch to the edit mode."""
        self.edit.setText(self.label.text())
        self.edit.setFont(self.label.font())
        self.layout.setCurrentWidget(self.edit)
        self.edit.setFocus()
        self.edit.selectAll()

    def _hide_edit(self):
        """Switch back to the label mode."""
        self.label.setText(self.edit.toPlainText() or self.label.text())
        self.layout.setCurrentWidget(self.label)

    def set_text(self, text: str):
        self.label.setText(text)

    def get_text(self) -> str:
        return self.label.text()
