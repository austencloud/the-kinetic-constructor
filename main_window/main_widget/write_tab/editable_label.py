# editable_label.py
from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt

class EditableLabel(QWidget):
    def __init__(self, label_text: str, parent=None):
        super().__init__(parent)
        self.label = QLabel(label_text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.edit = QLineEdit(self)
        self.edit.setPlaceholderText(label_text)
        self.edit.setVisible(False)
        self.edit.returnPressed.connect(self._hide_edit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        self.label.mousePressEvent = self._show_edit  # Clicking the label will trigger editing

    def _show_edit(self, event):
        """Show the QLineEdit for editing."""
        self.label.setVisible(False)
        self.edit.setVisible(True)
        self.edit.setFocus()

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
