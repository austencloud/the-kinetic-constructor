from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QScreen
from PyQt6.QtCore import Qt

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


class SplashScreen(QWidget):
    def __init__(self, target_screen: QScreen):
        super().__init__()

        # Set up splash screen window
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: white;")

        # Calculate the size of the splash screen (1/4 of the screen size)
        screen_geometry = target_screen.geometry()
        splash_screen_width = int(screen_geometry.width() // 2.5)
        splash_screen_height = int(screen_geometry.height() // 2.5)

        # Set the splash screen size
        self.setFixedSize(splash_screen_width, splash_screen_height)

        # Layout for the splash screen (horizontal layout for left and right sections)
        layout = QHBoxLayout(self)

        # Left side (progress bar and text)
        left_layout = QVBoxLayout()

        # Add loading message
        self.title_label = QLabel("The Kinetic Constructor")
        title_label_font_size = int(splash_screen_height / 15)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Monotype Corsiva", title_label_font_size))

        # Add message label
        currently_loading_label_font_size = int(splash_screen_height / 40)
        self.currently_loading_label = QLabel("")
        self.currently_loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.currently_loading_label.setFont(
            QFont("Arial", currently_loading_label_font_size)
        )

        # Add progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Add clickable website link
        self.info_label = QLabel("Created by Austen Cloud")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(QFont("Arial", currently_loading_label_font_size))

        left_layout.addStretch(1)
        left_layout.addWidget(self.title_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.progress_bar)
        left_layout.addStretch(1)
        left_layout.addWidget(self.currently_loading_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.info_label)
        left_layout.addStretch(1)

        # Add the left layout to the main layout
        layout.addLayout(left_layout)

        # Right side (image/logo)
        splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))

        # Scale the image based on the screen size
        scaled_splash_pix = splash_pix.scaled(
            splash_screen_width // 2,
            splash_screen_height,
            Qt.AspectRatioMode.KeepAspectRatio,
        )
        logo_label = QLabel()
        logo_label.setPixmap(scaled_splash_pix)

        # Add the image to the right side of the layout
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignRight)

        self._center_on_screen(target_screen)
        self.show()

    def _center_on_screen(self, target_screen: QScreen):
        """Center the splash screen on the target screen."""
        screen_geometry = target_screen.geometry()
        self.setGeometry(
            screen_geometry.x() + (screen_geometry.width() - self.width()) // 2,
            screen_geometry.y() + (screen_geometry.height() - self.height()) // 2,
            self.width(),
            self.height(),
        )

    def update_progress(self, value, message=""):
        """Update progress bar and message."""
        self.progress_bar.setValue(value)
        if message:
            self.currently_loading_label.setText(message)

    def finish(self):
        """Close the splash screen and show the main window."""
        self.close()
