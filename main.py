import sys
import cProfile
import pstats
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from widgets.main_widget import MainWidget
from settings.numerical_constants import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
from PyQt6.QtCore import QRect
from typing import IO

class MainWindow(QMainWindow):
    graph_editor_layout: 'QHBoxLayout'
    sequence_layout: 'QHBoxLayout'
    
    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler: cProfile.Profile = profiler
        self.screen: QRect = QApplication.primaryScreen().geometry()

        self.init_main_window()
        self.init_ui()

    def init_main_window(self):
        self.setMinimumSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def init_ui(self):
        self.move(-(self.screen.width() + 500), 100)

    def write_profiling_stats_to_file(self, file_path: str):
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
