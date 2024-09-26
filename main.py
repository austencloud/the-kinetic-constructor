import sys
import logging

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

    app = QApplication(sys.argv)
    dev_environment = not getattr(sys, "frozen", False)
    screens = QGuiApplication.screens()
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    # Initialize settings manager before showing splash screen
    settings_manager = SettingsManager(None)  # No main_window yet

    # Create and show the splash screen, passing the settings manager to set the background
    splash_screen = SplashScreen(target_screen, settings_manager)
    splash_screen.show()
    app.processEvents()  # Allows the splash screen to be rendered properly

    profiler = Profiler()

    # Create the main window and pass in the splash screen and settings manager
    from main_window.main_window import MainWindow

    main_window = MainWindow(profiler, splash_screen)

    # Finalize splash screen once initialization is complete
    main_window.show()
    QTimer.singleShot(0, lambda: splash_screen.close())
    sys.exit(main_window.exec(app))


if __name__ == "__main__":
    main()
