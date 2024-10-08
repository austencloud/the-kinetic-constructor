from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt
from typing import Callable, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class CheckboxDialog(QDialog):
    def __init__(
        self,
        parent: "QWidget",
        options: dict[str, bool],
        callback: Callable[[str, bool], None],
    ):
        super().__init__(
            parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.callback = callback
        self.checkboxes = {}
        self._setup_ui(options)

    def _setup_ui(self, options: dict[str, bool]):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        for option, checked in options.items():
            checkbox = QCheckBox(option)
            checkbox.setChecked(checked)
            checkbox.stateChanged.connect(
                lambda state, o=option: self.checkbox_toggled(o, state)
            )
            layout.addWidget(checkbox)
            self.checkboxes[option] = checkbox
        self.setLayout(layout)
        self.adjustSize()
        self.setStyleSheet(
            """
            QDialog {
                border: 2px solid black;
                border-radius: 5px;
                background-color: white;
            }
            QCheckBox {
                padding: 5px;
            }
            """
        )

    def checkbox_toggled(self, option: str, state):
        # Corrected comparison
        is_checked = state == Qt.CheckState.Checked.value
        self.callback(option, is_checked)

    def show_dialog(self, widget: "QWidget"):
        # Position the dialog below the widget
        global_pos = widget.mapToGlobal(widget.rect().bottomLeft())
        self.move(global_pos)
        self.exec()
