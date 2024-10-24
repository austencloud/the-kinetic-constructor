from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class EditableLabel(QWidget):
    def __init__(self, text="Label", parent=None):
        super().__init__(parent)
        self.label = QLabel(text, self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(text)
        self.line_edit.setVisible(False)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.setLayout(self.layout)

        self.label.mousePressEvent = self._edit_label
        self.line_edit.returnPressed.connect(self._save_label)

    def _edit_label(self, event):
        self.label.setVisible(False)
        self.line_edit.setVisible(True)
        self.line_edit.setFocus()

    def _save_label(self):
        text = self.line_edit.text()
        self.label.setText(text)
        self.label.setVisible(True)
        self.line_edit.setVisible(False)
