import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QEvent
from path_helpers import get_images_and_data_path
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
        self.setWindowTitle("TKA Constructor")
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

    # Load and scale the splash screen image
    splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))
    scaled_splash_pix = splash_pix.scaled(
        600, 400, Qt.AspectRatioMode.KeepAspectRatio
    )  # Adjust size as needed
    splash = QSplashScreen(scaled_splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(
        Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
    )
    splash.showMessage(
        "Initializing...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )
    splash.show()

    app.processEvents()  # Ensure the splash screen is displayed immediately

    steps = 4  # Example number of steps for the loading process
    profiler = Profiler()

    # Step 1
    splash.showMessage(
        "Setting up the main interface...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white,
    )
    app.processEvents()
    main_window = MainWindow(profiler)

    # Additional steps...
    for step in range(2, steps + 1):
        splash.showMessage(
            f"Loading step {step} of {steps}...",
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
            Qt.GlobalColor.white,
        )
        app.processEvents()
        # Simulate some loading tasks or setup operations here

    splash.finish(main_window)
    exit_code = main_window.exec_with_profiling(app)

    root_directory = os.path.dirname(os.path.abspath(__file__))
    profiler.write_profiling_stats_to_file("main_profiling_stats.txt", root_directory)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
