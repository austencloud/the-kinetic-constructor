import sys
import os
import cProfile
import pstats
from typing import IO
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PyQt6.QtCore import QRect
from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    graph_editor_layout: QHBoxLayout
    sequence_layout: QHBoxLayout

    def __init__(self, profiler: cProfile.Profile) -> None:
        super().__init__()
        self.profiler = profiler

        # Detecting screen setup
        self.screens = QApplication.screens()
        self.multi_screen_logic_needed = self.check_multi_screen_logic()

        # Apply multi-screen logic if necessary
        if self.multi_screen_logic_needed:
            self.apply_multi_screen_logic()
        else:
            self.apply_single_screen_logic()

        self.init_main_window()
        self.init_ui()

    def check_multi_screen_logic(self) -> bool:
        # Determine if multi-screen adjustments are needed
        return len(self.screens) > 1

    def apply_multi_screen_logic(self) -> None:
        # Logic for multiple screens
        self.screen = QApplication.primaryScreen()
        scaling_factor = self.screen.devicePixelRatio()
        self.scaled_screen_width = self.screen.geometry().width() * scaling_factor
        self.scaled_screen_height = self.screen.geometry().height() * scaling_factor

        # Calculate dynamic size based on scaled screen dimensions
        self.main_window_width = int(self.screen.geometry().width() * 0.4)
        self.main_window_height = int(self.screen.geometry().height() * 0.85)

    def apply_single_screen_logic(self) -> None:
        # Logic for a single screen
        self.screen = QApplication.primaryScreen()
        self.main_window_width = int(self.screen.geometry().width() * 0.6)
        self.main_window_height = int(self.screen.geometry().height() * 0.7)

    def init_main_window(self) -> None:
        self.setMinimumSize(self.main_window_width, self.main_window_height)
        self.main_widget = MainWidget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Constructor")

    def init_ui(self) -> None:
        if self.multi_screen_logic_needed:
            # Center the window on the second screen to the left if multiple screens are detected
            screen_number = 1 if len(self.screens) > 1 else 0
            screen_geometry = self.screens[screen_number].geometry()
            self.move(
                screen_geometry.x()
                + (screen_geometry.width() - self.main_window_width) // 2,
                screen_geometry.y()
                + (screen_geometry.height() - self.main_window_height) // 2,
            )
        else:
            self.setGeometry(
                QRect(
                    (self.screen.geometry().width() - self.main_window_width) // 2,
                    (self.screen.geometry().height() - self.main_window_height) // 2,
                    self.main_window_width,
                    self.main_window_height,
                )
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
