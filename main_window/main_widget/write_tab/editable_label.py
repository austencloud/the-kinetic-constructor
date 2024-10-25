from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class EditableLabel(QWidget):
    def __init__(self, label_text: str, parent=None):
        super().__init__(parent)
        self.label = QLabel(label_text, self)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Customize QLineEdit to match QLabel style initially
        self.edit = QLineEdit(self)
        self.edit.setVisible(False)
        self.edit.returnPressed.connect(self._hide_edit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        # Clicking the label will trigger editing
        self.label.mousePressEvent = self._show_edit

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current text pre-filled."""
        # Pre-fill with current text and align it in the center
        self.edit.setText(self.label.text())
        # self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Copy the current font and styles to the edit box
        current_font = self.label.font()
        self.edit.setFont(current_font)

        # Show edit and hide label
        self.label.setVisible(False)
        self.edit.setVisible(True)
        self.edit.setFocus()
        # select all the text
        self.edit.selectAll()

    def _hide_edit(self):
        """Hide the QLineEdit and show the QLabel."""
        new_text = self.edit.text()
        self.label.setText(new_text if new_text else self.label.text())
        self.label.setVisible(True)
        self.edit.setVisible(False)

    def set_text(self, text: str):
        """Programmatically set the text of the label."""
        self.label.setText(text)

    def get_text(self) -> str:
        """Get the current text of the label."""
        return self.label.text()

    def resizeEvent(self, event):
        """Resize the QLineEdit to match the QLabel size."""
        self.edit.resize(self.label.size())
        # font_size = self.label.font().pointSize()
        self.edit.setStyleSheet(
            # center it
            # f"font-size: {font_size}pt;"
            "border: none;"
            "background-color: rgba(0, 0, 0, 0);"
            "color: black;"
            "alignment: center;"
        )
        super().resizeEvent(event)
