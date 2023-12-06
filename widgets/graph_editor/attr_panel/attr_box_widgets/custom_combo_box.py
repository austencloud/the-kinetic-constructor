from typing import TYPE_CHECKING
from settings.string_constants import (
    ICON_DIR,
)

if TYPE_CHECKING:
    pass
from PyQt6.QtWidgets import QComboBox



class CustomComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        combobox_border = 2
        self.setStyleSheet(
            f"""
            QComboBox {{
                border: {combobox_border}px solid black;
                border-radius: 10px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px; /* Width of the arrow */
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* Just a single line */
                border-top-right-radius: 3px; /* Same radius as QComboBox */
                border-bottom-right-radius: 3px;
            }}

            QComboBox::down-arrow {{
                image: url("{ICON_DIR}combobox_arrow.png"); /* Path to your custom arrow icon */
                width: 10px; /* Width of the icon */
                height: 10px; /* Height of the icon */
            }}
        """
        )
