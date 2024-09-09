import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtCore import Qt
from utilities.path_helpers import get_images_and_data_path


class SplashScreen(QSplashScreen):
    def __init__(self, target_screen: QScreen):
        """Initialize the splash screen."""
        splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
        scaled_splash_pix = splash_pix.scaled(
            600, 400, Qt.AspectRatioMode.KeepAspectRatio
        )
        super().__init__(scaled_splash_pix, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        
        self._center_on_screen(target_screen)
        self.show_message()

    def _center_on_screen(self, target_screen: QScreen):
        """Center the splash screen on the target screen."""
        self.setGeometry(
            target_screen.geometry().x()
            + (target_screen.geometry().width() - self.pixmap().width()) // 2,
            target_screen.geometry().y()
            + (target_screen.geometry().height() - self.pixmap().height()) // 2,
            self.pixmap().width(),
            self.pixmap().height(),
        )

    def show_message(self):
        """Display a message on the splash screen."""
        self.showMessage(
            "Initializing...",
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
            Qt.GlobalColor.white,
        )

    def finish(self, main_window):
        """Finish and close the splash screen once the main window is ready."""
        super().finish(main_window)
