import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QGuiApplication
from widgets.main_widget import MainWidget
from profiler import Profiler
import os


class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler) -> None:
        super().__init__()
        self.profiler = profiler

        self._init_main_window()

    def _init_main_window(self) -> None:
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Sequence Constructor")
        self.show()

    def _set_dimensions(self):
        screens = QGuiApplication.screens()
        screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()
        window_width = self.main_widget.width()
        window_height = self.main_widget.height()
        x = available_geometry.x() + (available_geometry.width() - window_width) // 2
        y = available_geometry.y() + (available_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

    def exec_with_profiling(self, app: QApplication) -> int:
        for func in [app.exec, self.show]:
            self.profiler.runcall(func)


def main() -> None:
    app = QApplication(sys.argv)
    profiler = Profiler()
    main_window = MainWindow(profiler)
    main_window.setFocus()
    main_window._set_dimensions()
    exit_code = main_window.exec_with_profiling(app)
    root_directory = os.path.abspath(os.sep)
    # Get the directory of the main script
    root_directory = os.path.dirname(os.path.abspath(__file__))

    main_window.profiler.write_profiling_stats_to_file(
        "main_profiling_stats.txt", root_directory
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
