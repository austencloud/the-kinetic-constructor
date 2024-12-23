from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
)
from PyQt6.QtGui import QFont, QIcon, QDesktopServices
from PyQt6.QtCore import Qt, QSize, QUrl

from main_window.menu_bar_widget.base_selector import BaseSelector
from .user_profile_selector import UserProfileSelector
from .background_selector.background_selector import BackgroundSelector
from .prop_type_selector import PropTypeSelector
from .grid_mode_selector import GridModeSelector
from .visibility_selector import VisibilitySelector

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MenuBarWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

        # Initialize selectors
        self.user_profile_selector = UserProfileSelector(self)
        self.prop_type_selector = PropTypeSelector(self)
        # self.grid_mode_selector = GridModeSelector(self)
        self.background_selector = BackgroundSelector(self)
        self.visibility_selector = VisibilitySelector(self)

        # Create labels for selectors
        self.user_profile_label = QLabel("User:")
        self.prop_type_label = QLabel("Prop:")
        self.grid_mode_label = QLabel("Grid:")
        self.background_label = QLabel("Background:")
        self.visibility_label = QLabel("")

        self.sections: list[tuple[QLabel, BaseSelector]] = [
            (self.user_profile_label, self.user_profile_selector),
            (self.prop_type_label, self.prop_type_selector),
            # (self.grid_mode_label, self.grid_mode_selector),
            (self.background_label, self.background_selector),
            (self.visibility_label, self.visibility_selector),
        ]

        # Set all the labels to be centered horizontally
        for label in self.sections:
            label[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels = [label for label, _ in self.sections]
        self.separators: list[QFrame] = []
        self.layout: QHBoxLayout = QHBoxLayout(self)

        self.layout.addStretch(1)

        # Add the social buttons (now arranged in two rows)
        self.add_social_buttons()

        # Add selectors with labels and separators
        for i, (label, selector) in enumerate(self.sections):
            self.add_separator()  # Add separator before each section
            self.add_section(label, selector)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def add_social_buttons(self):
        # Create a grid layout to hold the buttons in two rows
        self.social_buttons_grid = QGridLayout()
        self.social_buttons_grid.setSpacing(10)
        self.social_buttons_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the buttons
        self.paypal_button = self.create_icon_button(
            icon_path="images/icons/paypal.png",
            tooltip="Support via PayPal",
            click_handler=self.open_paypal_link,
        )

        self.venmo_button = self.create_icon_button(
            icon_path="images/icons/venmo.png",
            tooltip="Support via Venmo",
            click_handler=self.open_venmo_link,
        )

        self.github_button = self.create_icon_button(
            icon_path="images/icons/github.png",
            tooltip="View project on GitHub",
            click_handler=self.open_github_link,
        )

        self.facebook_button = self.create_icon_button(
            icon_path="images/icons/facebook.png",
            tooltip="Visit on Facebook",
            click_handler=self.open_facebook_link,
        )

        self.instagram_button = self.create_icon_button(
            icon_path="images/icons/instagram.png",
            tooltip="Follow on Instagram",
            click_handler=self.open_instagram_link,
        )

        # Add an additional button (e.g., Twitter)
        self.youtube_button = self.create_icon_button(
            icon_path="images/icons/youtube.png",
            tooltip="Follow on YouTube",
            click_handler=self.open_youtube_link,
        )

        # List of buttons
        self.social_buttons = [
            self.paypal_button,
            self.venmo_button,
            self.github_button,
            self.facebook_button,
            self.instagram_button,
            self.youtube_button,
        ]

        # Add buttons to the grid layout (two rows of three buttons)
        for index, button in enumerate(self.social_buttons):
            row = index // 3  # 0 or 1
            col = index % 3  # 0, 1, or 2
            self.social_buttons_grid.addWidget(button, row, col)

        # Create a widget to hold the grid layout
        self.social_buttons_widget = QWidget()
        self.social_buttons_widget.setLayout(self.social_buttons_grid)

        # Create a vertical layout to center the social buttons vertically
        self.social_buttons_container = QVBoxLayout()
        self.social_buttons_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.social_buttons_container.addWidget(self.social_buttons_widget)

        # Add the social buttons container to the main layout
        self.layout.addLayout(self.social_buttons_container)

    def create_icon_button(self, icon_path, tooltip, click_handler):
        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set the icon
        icon = QIcon(icon_path)
        button.setIcon(icon)

        # Set the icon size
        icon_size = QSize(
            self.main_widget.height() // 40, self.main_widget.height() // 40
        )
        button.setIconSize(icon_size)
        button.setFixedSize(icon_size.width() + 10, icon_size.height() + 10)

        # Style the button
        button.setStyleSheet(
            """
            QPushButton {
                border: none;
                background-color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """
        )
        button.setToolTip(tooltip)

        # Connect the click event
        button.clicked.connect(click_handler)

        return button

    def open_paypal_link(self):
        paypal_url = QUrl(
            "https://www.paypal.me/austencloud"
        )  # Replace with your PayPal link
        QDesktopServices.openUrl(paypal_url)

    def open_venmo_link(self):
        venmo_url = QUrl("https://venmo.com/austencloud")
        QDesktopServices.openUrl(venmo_url)

    def open_github_link(self):
        github_url = QUrl("https://github.com/austencloud/the-kinetic-constructor")
        QDesktopServices.openUrl(github_url)

    def open_facebook_link(self):
        facebook_url = QUrl(
            "https://www.facebook.com/austencloud"
        )  # Replace with your Facebook page
        QDesktopServices.openUrl(facebook_url)

    def open_instagram_link(self):
        instagram_url = QUrl("https://www.instagram.com/thekineticalphabet")
        QDesktopServices.openUrl(instagram_url)

    def open_youtube_link(self):
        youtube_url = QUrl("https://youtube.com/austencloud")
        QDesktopServices.openUrl(youtube_url)

    def add_section(self, label: QLabel, selector: QWidget):
        section_layout = QVBoxLayout()
        section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.setSpacing(2)  # Minimal vertical spacing
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.addWidget(label)
        section_layout.addWidget(selector)
        self.layout.addLayout(section_layout)

    def add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        self.layout.addWidget(separator)
        self.separators.append(separator)

    def resize_menu_bar_widget(self):
        self.menu_bar_font_size = self.main_widget.width() // 120
        spacing = self.width() // 40  # Horizontal spacing between sections
        self.layout.setSpacing(spacing)
        font_size = self.main_widget.width() // 145
        for label in self.labels:
            font = QFont("Georgia", font_size)
            label.setFont(font)

        # Style selectors
        for _, selector in self.sections:
            selector.style_widget()

        for separator in self.separators:
            separator.setLineWidth(1)
        self.setMaximumWidth(self.main_widget.width())

        # Update icon sizes on resize
        icon_size = QSize(
            self.main_widget.height() // 40, self.main_widget.height() // 40
        )
        for button in self.social_buttons:
            button.setIconSize(icon_size)
            button.setFixedSize(icon_size.width() + 10, icon_size.height() + 10)
