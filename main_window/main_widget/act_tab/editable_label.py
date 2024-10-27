from PyQt6.QtWidgets import QLabel, QLineEdit, QWidget, QStackedLayout, QSizePolicy
from PyQt6.QtCore import Qt


class EditableLabel(QWidget):
    def __init__(self, parent, label_text: str):
        super().__init__(parent)
        self.label = QLabel(label_text, self)
        self.edit = QLineEdit(self)
        self.edit.returnPressed.connect(self._hide_edit)


        # Remove padding and margins in style sheets
        self.label.setStyleSheet(
            # "border-top: 1px solid black;"
            # "border-bottom: 1px solid black;"
            "padding: 0px;"
            "margin: 0px;"
        )
        self.edit.setStyleSheet(
            # "border-top: 1px solid black;"
            # "border-bottom: 1px solid black;"
            "padding: 0px;"
            "margin: 0px;"
        )

        # Remove contents margins
        self.label.setContentsMargins(0, 0, 0, 0)
        self.edit.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        # Use QStackedLayout to switch between label and edit
        self.layout: QStackedLayout = QStackedLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.setLayout(self.layout)

        # Assign the mouse press event to show the editor
        self.label.mousePressEvent = self._show_edit

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current text pre-filled."""
        self.edit.setText(self.label.text())
        current_font = self.label.font()
        self.edit.setFont(current_font)

        # Switch to the edit widget
        self.layout.setCurrentWidget(self.edit)

        self.edit.setFocus()
        self.edit.selectAll()

    def _hide_edit(self):
        """Hide the QLineEdit and show the QLabel."""
        new_text = self.edit.text()
        self.label.setText(new_text if new_text else self.label.text())

        # Switch back to the label widget
        self.layout.setCurrentWidget(self.label)

    def set_text(self, text: str):
        """Programmatically set the text of the label."""
        self.label.setText(text)

    def get_text(self) -> str:
        """Get the current text of the label."""
        return self.label.text()
