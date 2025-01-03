from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from .user_profile_tab import UserProfileTab
from .prop_type_tab import PropTypeTab
from .background_tab import BackgroundTab
from .visibility_tab import VisibilityTab
if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

class SettingsDialog(QDialog):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setWindowTitle("Settings")

        # Dynamically size the dialog to half the main widget size
        main_widget_size = main_widget.size()
        self.setFixedSize(main_widget_size.width() // 2, main_widget_size.height() // 2)

        self._setup_ui()

    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Tab widget for categorized settings
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        # Add tabs
        self.tab_widget.addTab(UserProfileTab(self.main_widget), "User Profile")
        self.tab_widget.addTab(PropTypeTab(self.main_widget), "Prop Type")
        self.tab_widget.addTab(BackgroundTab(self.main_widget), "Background")
        self.tab_widget.addTab(VisibilityTab(self.main_widget), "Visibility")

        # Add a Save and Close button at the bottom
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )

        save_button = QPushButton("Save")
        save_button.setFont(self._get_default_font())
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        close_button = QPushButton("Close")
        close_button.setFont(self._get_default_font())
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
