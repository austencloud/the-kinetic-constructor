import sys
import logging

from welcome_dialog import WelcomeDialog

logging.basicConfig(level=logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer
from profiler import Profiler
from splash_screen import SplashScreen
from main_window.settings_manager.settings_manager import SettingsManager


def main() -> None:
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)


def main() -> None:
    app = QApplication(sys.argv)
    dev_environment = not getattr(sys, "frozen", False)
    screens = QGuiApplication.screens()
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    settings_manager = SettingsManager(None)  # Initialize settings

    # Show the splash screen as usual
    splash_screen = SplashScreen(target_screen, settings_manager)
    splash_screen.show()
    app.processEvents()

    # Continue with the rest of the program initialization
    profiler = Profiler()
    from main_window.main_window import MainWindow

    main_window = MainWindow(profiler, splash_screen)
    main_window.show()

    QTimer.singleShot(0, lambda: splash_screen.close())
    # Check if we should show the welcome screen

    welcome_dialog = WelcomeDialog(settings_manager, main_window)
    welcome_dialog.exec()
    welcome_dialog.raise_()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
