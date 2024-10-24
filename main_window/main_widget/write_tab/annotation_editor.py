# annotation_editor.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel

if TYPE_CHECKING:
    from .write_tab import WriteTab


class AnnotationEditor(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.annotation_label = QLabel("Annotations / Lyrics", self)
        self.annotation_text = QTextEdit(self)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.annotation_label)
        layout.addWidget(self.annotation_text)
        self.setLayout(layout)

    def resize_editor(self):
        # Adjust size based on parent widget size
        pass
