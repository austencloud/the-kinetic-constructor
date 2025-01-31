import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from main_window.settings_manager.settings_manager import SettingsManager
from splash_screen.splash_screen import SplashScreen
from main_window.main_window import MainWindow
from profiler import Profiler


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    settings_manager = SettingsManager(None)
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()
    profiler = Profiler()
    main_window = MainWindow(profiler, splash_screen)
    main_window.show()
    main_window.raise_()

    QTimer.singleShot(0, lambda: splash_screen.close())
    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
