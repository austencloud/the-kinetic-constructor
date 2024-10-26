from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class EditableLabel(QWidget):
    def __init__(self, parent, label_text: str):
        super().__init__(parent)
        self.label = QLabel(label_text, self)
        self.edit = QLineEdit(self)
        self.edit.setVisible(False)
        self.edit.returnPressed.connect(self._hide_edit)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        self.label.mousePressEvent = self._show_edit

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current text pre-filled."""
        self.edit.setText(self.label.text())
        current_font = self.label.font()
        self.edit.setFont(current_font)
        
        self.label.setVisible(False)
        self.edit.setVisible(True)
        
        self.edit.setFocus()
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
        self.edit.setStyleSheet(
            "border: none;"
            "background-color: rgba(0, 0, 0, 0);"
            "color: black;"
            "alignment: center;"
        )
        super().resizeEvent(event)
