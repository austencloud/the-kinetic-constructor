import sys
import os
import cProfile
import pstats
from typing import IO
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PyQt6.QtCore import QRect
from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    graph_editor_layout: "QHBoxLayout"
    sequence_layout: "QHBoxLayout"

    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler = profiler

        self.screen = QApplication.primaryScreen()
        scaling_factor = self.screen.devicePixelRatio()
        self.scaled_screen_width = self.screen.geometry().width() * scaling_factor
        self.scaled_screen_height = self.screen.geometry().height() * scaling_factor

        # Calculate dynamic size based on scaled screen dimensions
        self.main_window_width = int(self.screen.geometry().width() * 0.4)
        self.main_window_height = int(self.screen.geometry().height() * 0.8)

        self.init_main_window()
        self.init_ui()


    def get_current_width(self) -> int:
        # Get the  width of the main window, intended for use after the resize has occured so I can't just resue a previously made value
        return self.width()
    

    def init_main_window(self) -> None:
        self.setMinimumSize(self.main_window_width, self.main_window_height)
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def init_ui(self) -> None:
        # Center the window on the second screen to the left
        screen_number = 1
        screen_geometry = QApplication.screens()[screen_number].geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.move(
            0 - int(self.scaled_screen_width) + int(self.main_window_width / 2),
            screen_geometry.top() + int(screen_height / 2 - self.main_window_height / 2),
        )

    def write_profiling_stats_to_file(self, file_path: str) -> None:
        stats: pstats.Stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        with open(file_path, "w") as f:
            stats.stream: IO[str] = f
            stats.print_stats()
        print(f"Main profiling stats written to {file_path}")


def main() -> None:
    profiler: cProfile.Profile = cProfile.Profile()
    profiler.enable()

    # Set the environment variable for automatic screen scaling
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
