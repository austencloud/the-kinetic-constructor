import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtCore import Qt
from utilities.path_helpers import get_images_and_data_path


class SplashScreenManager:
    def __init__(self, target_screen: QScreen):
        self.splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
        self.scaled_splash_pix = self.splash_pix.scaled(
            600, 400, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.splash = QSplashScreen(
            self.scaled_splash_pix,
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint,
        )
        self._center_on_screen(target_screen)
        self.show()

    def _center_on_screen(self, target_screen: QScreen):
        """Center the splash screen on the target screen."""
        self.splash.setGeometry(
            target_screen.geometry().x()
            + (target_screen.geometry().width() - self.scaled_splash_pix.width()) // 2,
            target_screen.geometry().y()
            + (target_screen.geometry().height() - self.scaled_splash_pix.height())
            // 2,
            self.scaled_splash_pix.width(),
            self.scaled_splash_pix.height(),
        )

    def show(self):
        """Show the splash screen with a message."""
        self.splash.showMessage(
            "Initializing...",
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
            Qt.GlobalColor.white,
        )
        self.splash.show()

    def finish(self, main_window):
        """Finish and close the splash screen once the main window is ready."""
        self.splash.finish(main_window)
