import sys
import logging

from splash_screen import SplashScreenManager

logging.basicConfig(level=logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer
from main_window.main_window import MainWindow
from profiler import Profiler


def main() -> None:
    app = QApplication(sys.argv)
    dev_environment = not getattr(sys, "frozen", False)
    screens = QGuiApplication.screens()
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    splash_manager = SplashScreenManager(target_screen)

    app.processEvents()

    profiler = Profiler()
    main_window = MainWindow(profiler)
    main_window.show()

    QTimer.singleShot(0, lambda: splash_manager.finish(main_window))

    sys.exit(main_window.exec(app))


if __name__ == "__main__":
    main()
