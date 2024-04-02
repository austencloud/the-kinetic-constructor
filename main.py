import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QEvent
from profiler import Profiler
from settings_manager import SettingsManager
from utilities.main_window_geometry_manager import MainWindowGeometryManager
from widgets.main_widget.main_widget import MainWidget
from widgets.menu_bar.menu_bar import MainWindowMenuBar


class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler) -> None:
        super().__init__()
        self.profiler = profiler
        self.settings_manager = SettingsManager(self)
        self.main_widget = MainWidget(self)
        self.main_widget.preferences_dialog.load_initial_settings()
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.window_manager = MainWindowGeometryManager(self)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Kinetic Constructor")
        self.menu_bar = MainWindowMenuBar(self.main_widget)
        self.setMenuBar(self.menu_bar)
        self.show()

    def exec_with_profiling(self, app: QApplication) -> int:
        for func in [app.exec, self.show]:
            self.profiler.runcall(func)
        return 0

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        super().closeEvent(event)
        QApplication.instance().installEventFilter(self)


def main() -> None:
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap(
        "path/to/splash_image.jpg"
    )  # Specify the path to your splash image
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(
        Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
    )
    splash.showMessage(
        "Loading...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )
    splash.show()

    # Ensure the splash screen is displayed immediately
    app.processEvents()

    # Initialize your main window here (heavy lifting)
    profiler = Profiler()
    main_window = MainWindow(profiler)
    splash.showMessage(
        "Setting up the main interface...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )

    # Example of updating the splash screen with new messages
    splash.showMessage(
        "Loading modules...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )

    # Finish splash and show the main window
    splash.finish(main_window)
    exit_code = main_window.exec_with_profiling(app)

    # Your existing code for profiling and exit
    root_directory = os.path.dirname(os.path.abspath(__file__))
    profiler.write_profiling_stats_to_file("main_profiling_stats.txt", root_directory)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
