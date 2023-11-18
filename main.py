import sys
import os
import cProfile
import pstats
from typing import IO
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PyQt6.QtCore import QRect
from widgets.main_widget import MainWidget
from PyQt6.QtGui import QScreen


class MainWindow(QMainWindow):
    graph_editor_layout: QHBoxLayout
    sequence_layout: QHBoxLayout
    optionboard_layout: QHBoxLayout

    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler = profiler

        self.configure_window()
        self.init_main_window()
        self.init_ui()

    def configure_window(self) -> None:
        screens = QApplication.screens()
        primary_screen = screens[0]
        secondary_screen = screens[1] if len(screens) > 1 else primary_screen

        scaling_factor = primary_screen.devicePixelRatio()
        screen_geometry = secondary_screen.geometry()

        # Adjust size based on the screen used
        self.main_window_width = int(
            screen_geometry.width() * (0.8 if len(screens) > 1 else 0.6)
        )
        self.main_window_height = int(
            screen_geometry.height() * (0.8 if len(screens) > 1 else 0.7)
        )

        # Positioning the window
        self.move(
            screen_geometry.x()
            + (screen_geometry.width() - self.main_window_width) // 2
            - 50,
            screen_geometry.y()
            + (screen_geometry.height() - self.main_window_height) // 2
            - 50,
        )

    def init_main_window(self) -> None:
        self.setMinimumSize(self.main_window_width, self.main_window_height)
        self.resize(self.width(), self.height())
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def init_ui(self) -> None:
        # Any additional UI initialization goes here
        pass

    def write_profiling_stats_to_file(self, file_path: str) -> None:
        stats: pstats.Stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        with open(file_path, "w") as f:
            stats.stream: IO[str] = f
            stats.print_stats()
        print(f"Main profiling stats written to {file_path}")


def main() -> None:
    profiler: cProfile.Profile = cProfile.Profile()
    profiler.enable()

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    main_window = MainWindow(profiler)
    main_window.setFocus()
    exit_code = app.exec()

    profiler.disable()
    main_window.write_profiling_stats_to_file("main_profiling_stats.txt")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
