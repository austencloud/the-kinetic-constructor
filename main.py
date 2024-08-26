import sys
import logging
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QGuiApplication, QScreen
from PyQt6.QtCore import Qt, QTimer
from main_window.main_window import MainWindow
from widgets.path_helpers.path_helpers import get_images_and_data_path
from widgets.profiler import Profiler

logging.getLogger("PIL").setLevel(logging.WARNING)


def main() -> None:
    app = QApplication(sys.argv)
    screens = QGuiApplication.screens()
    dev_environment = not getattr(sys, "frozen", False)
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    app.processEvents()

    profiler = Profiler()
    main_window = MainWindow(profiler)
    splash = _show_splash_screen(target_screen)
    main_window.show()

    QTimer.singleShot(1000, lambda: splash.finish(main_window))

    sys.exit(main_window.exec(app))


def _show_splash_screen(target_screen: QScreen) -> QSplashScreen:
    splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
    scaled_splash_pix = splash_pix.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(
        scaled_splash_pix,
        Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint,
    )

    splash.setGeometry(
        target_screen.geometry().x()
        + (target_screen.geometry().width() - scaled_splash_pix.width()) // 2,
        target_screen.geometry().y()
        + (target_screen.geometry().height() - scaled_splash_pix.height()) // 2,
        scaled_splash_pix.width(),
        scaled_splash_pix.height(),
    )
    splash.showMessage(
        "Initializing...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )
    splash.show()
    return splash


if __name__ == "__main__":
    main()
