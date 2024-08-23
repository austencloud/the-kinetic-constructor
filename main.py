import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QTimer
from widgets.path_helpers.path_helpers import get_images_and_data_path
from widgets.profiler import Profiler
from settings_manager.settings_manager import SettingsManager
from utilities.main_window_geometry_manager import MainWindowGeometryManager
from widgets.main_widget.main_widget import MainWidget
from widgets.menu_bar.main_window_menu_bar import MainWindowMenuBar
import logging

logging.getLogger("PIL").setLevel(logging.WARNING)


class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler) -> None:
        super().__init__()
        self.profiler = profiler
        self.settings_manager = SettingsManager(self)
        self.main_widget = MainWidget(self)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.window_manager = MainWindowGeometryManager(self)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Kinetic Constructor")
        self.menu_bar = MainWindowMenuBar(self.main_widget)
        self.setMenuBar(self.menu_bar)

    def exec_with_profiling(self, app: QApplication) -> int:
        self.profiler.enable()
        result = app.exec()
        self.profiler.disable()
        self.profiler.write_profiling_stats_to_file("profiling_output.txt", os.getcwd())
        return result

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        super().closeEvent(event)
        QApplication.instance().installEventFilter(self)


def main() -> None:
    app = QApplication(sys.argv)

    # Get all available screens
    screens = QGuiApplication.screens()

    # Determine if the application is in development or production mode
    dev_environment = not getattr(sys, "frozen", False)

    # Select the appropriate screen based on the environment
    # Default to the primary screen in production or the second screen in development (if available)
    target_screen = screens[1] if dev_environment and len(screens) > 1 else screens[0]

    # Load and scale the splash screen image
    splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
    scaled_splash_pix = splash_pix.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(
        scaled_splash_pix,
        Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint,
    )

    # Move the splash to the center of the selected screen
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

    app.processEvents()  # Ensure the splash screen is displayed immediately

    # Create the main window and configure it
    profiler = Profiler()
    main_window = MainWindow(profiler)
    main_window.show()  # Display the main window

    QTimer.singleShot(1000, lambda: splash.finish(main_window))

    sys.exit(main_window.exec_with_profiling(app))


if __name__ == "__main__":
    main()
