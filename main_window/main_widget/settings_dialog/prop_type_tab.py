from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from Enums.PropTypes import PropType
if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog

class PropTypeTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self._setup_ui()


    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Prop Type Settings")
        title.setFont(self._get_title_font())
        layout.addWidget(title)

        prop_types = [
            "Hand",
            "Staff",
            "Club",
            "Fan",
            "Triad",
            "Minihoop",
            "Buugeng",
            "Sword",
            "Ukulele",
        ]

        for prop in prop_types:
            button = QPushButton(prop)
            button.setFont(self._get_default_font())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(
                lambda _, p=prop: self._set_current_prop_type(PropType.get_prop_type(p))
            )
            layout.addWidget(button)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def _set_current_prop_type(self, prop_type: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_prop_type(prop_type)
        self.main_widget.settings_manager.global_settings.prop_type_changer.apply_prop_type()

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
