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
if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BackgroundTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Background Settings")
        title.setFont(self._get_title_font())
        layout.addWidget(title)

        # Available background options
        backgrounds = ["Starfield", "Aurora", "Snowfall", "Bubbles"]

        for background in backgrounds:
            button = QPushButton(background)
            button.setFont(self._get_default_font())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, b=background: self._set_background(b))
            layout.addWidget(button)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        self.setLayout(layout)

    def _set_background(self, background: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_background_type(background)
        self.main_widget.background_widget.apply_background()

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
