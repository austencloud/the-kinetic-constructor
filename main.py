import sys
import cProfile
import pstats
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets.main_widget import MainWidget
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow
from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler = profiler

        self._configure_window()
        self._init_main_window()

    def _configure_window(self) -> None:
        screens = QGuiApplication.screens()
        if len(screens) > 1:
            screen = screens[1]
        else:
            screen = QGuiApplication.primaryScreen() 

        available_geometry = screen.availableGeometry()

        self.main_window_width = available_geometry.width() * 0.75
        self.main_window_height = available_geometry.height() * 0.75

        self.move(
            int(
                available_geometry.x()
                + (available_geometry.width() - self.main_window_width) / 2
            ),
            int(
                available_geometry.y()
                + (available_geometry.height() - self.main_window_height) / 2
            ),
        )


    def _init_main_window(self) -> None:
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Sequence Constructor")
        self._configure_window()
        self.show()
        

    def write_profiling_stats_to_file(self, file_path: str) -> None:
        stats: pstats.Stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        with open(file_path, "w") as f:
            stats.stream = f  # Add this line to set the output stream
            stats.print_stats()
        print(f"Main profiling stats written to {file_path}")


def main() -> None:
    """
    The entry point of the application.
    """
    profiler: cProfile.Profile = cProfile.Profile()
    profiler.enable()
    app = QApplication(sys.argv)
    main_window = MainWindow(profiler)
    main_window.setFocus()
    exit_code = app.exec()

    profiler.disable()
    main_window.write_profiling_stats_to_file("main_profiling_stats.txt")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
