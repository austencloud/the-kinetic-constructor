import sys
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPalette, QColor


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create and set a light color palette to override system defaults
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(225, 225, 225))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 163, 224))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    # Set up screen and development environment
    dev_environment = not getattr(sys, "frozen", False)
    screens = app.screens()
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    # Import SettingsManager after QApplication is initialized
    from main_window.settings_manager.settings_manager import SettingsManager
    settings_manager = SettingsManager(None)

    # Load SplashScreen with periodic QApplication processing
    from splash_screen.splash_screen import SplashScreen
    splash_screen = SplashScreen(target_screen, settings_manager)
    app.processEvents()

    # Load Profiler and MainWindow only after splash screen appears
    from profiler import Profiler
    profiler = Profiler()

    # Import MainWindow and ensure no blocking tasks in __init__
    from main_window.main_window import MainWindow
    main_window = MainWindow(profiler, splash_screen)
    main_window.show()

    # Close the splash screen after showing the main window
    QTimer.singleShot(0, lambda: splash_screen.close())

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
