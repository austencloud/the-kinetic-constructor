import sys
import logging
from typing import TYPE_CHECKING
import webbrowser
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
)
from PyQt6.QtGui import QPixmap, QFont, QScreen
from PyQt6.QtCore import Qt, QTimer
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

        # Main layout
        layout = QVBoxLayout(self)

        # Add image/logo to splash screen
        splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
        logo_label = QLabel()
        logo_label.setPixmap(
            splash_pix.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
        )
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add loading message
        self.message_label = QLabel("Initializing...")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(QFont("Arial", 12))
        self.message_label.setStyleSheet("color: black;")
        layout.addWidget(self.message_label)

        # Add progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Add clickable website link
        self.website_label = QLabel(
            "<a href='https://thekineticalphabet.com'>thekineticalphabet.com</a>"
        )
        self.website_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.website_label.setFont(QFont("Arial", 10))
        self.website_label.setStyleSheet("color: black;")
        self.website_label.setOpenExternalLinks(True)  # Makes the link clickable
        layout.addWidget(self.website_label)

        self._center_on_screen(target_screen)
        self.show()

    def _center_on_screen(self, target_screen: QScreen):
        """Center the splash screen on the target screen."""
        self.setGeometry(
            target_screen.geometry().x()
            + (target_screen.geometry().width() - self.width()) // 2,
            target_screen.geometry().y()
            + (target_screen.geometry().height() - self.height()) // 2,
            500,
            500,
        )

    def update_progress(self, value, message=""):
        """Update progress bar and message."""
        self.progress_bar.setValue(value)
        if message:
            self.message_label.setText(message)


