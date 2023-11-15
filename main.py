import sys
import cProfile
import pstats
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from widgets.main_widget import MainWidget
from PyQt6.QtCore import QRect
from typing import IO


class MainWindow(QMainWindow):
    graph_editor_layout: "QHBoxLayout"
    sequence_layout: "QHBoxLayout"
    
    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler: cProfile.Profile = profiler
        self.screen: QRect = QApplication.primaryScreen().geometry()

        # Calculate dynamic size based on screen dimensions
        self.main_window_width = int(self.screen.width() * 0.8)  # Example: 80% of screen width
        self.main_window_height = int(self.screen.height() * 0.8)  # Example: 80% of screen height

        self.init_main_window()
        self.init_ui()

    def init_main_window(self) -> None:
        self.setMinimumSize(self.main_window_width, self.main_window_height)
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def init_ui(self) -> None:
        # Center the window on the screen
        self.move((self.screen.width() - self.width()) // 2, (self.screen.height() - self.height()) // 2)

    def write_profiling_stats_to_file(self, file_path: str) -> None:
        stats: pstats.Stats = pstats.Stats(self.profiler).sort_stats("cumtime")
        with open(file_path, "w") as f:
            stats.stream: IO[str] = f
            stats.print_stats()
        print(f"Main profiling stats written to {file_path}")


def main() -> None:
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
