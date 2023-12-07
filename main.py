import sys
import os
import cProfile
import pstats
from typing import IO
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler = profiler

        self._configure_window()
        self._init_main_window()

    def _configure_window(self) -> None:
        screens = QApplication.screens()
        if len(screens) > 1:
            screen = screens[1] 
        else:
            screen = QApplication.primaryScreen()

        screen_geometry = screen.geometry()

        self.main_window_width = int(screen_geometry.width() * 0.9)
        self.main_window_height = int(screen_geometry.height() * 0.8)

        self.move(
            screen_geometry.x()
            + (screen_geometry.width() - self.main_window_width) // 2
            - 50,
            screen_geometry.y()
            + (screen_geometry.height() - self.main_window_height) // 2
            - 50,
        )

    def _init_main_window(self) -> None:
        self.setMinimumSize(self.main_window_width, self.main_window_height)
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def write_profiling_stats_to_file(self, file_path: str) -> None:
        stats: pstats.Stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        with open(file_path, "w") as f:
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
