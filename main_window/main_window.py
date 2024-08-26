import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt

from .menu_bar_widget import MenuBarWidget
from .settings_manager.settings_manager import SettingsManager
from .main_widget.main_widget import MainWidget
from widgets.profiler import Profiler
from main_window.main_window_geometry_manager import MainWindowGeometryManager


class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler) -> None:
        super().__init__()
        self.profiler = profiler
        self.settings_manager = SettingsManager(self)
        self.main_widget = MainWidget(self)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.window_manager = MainWindowGeometryManager(self)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Kinetic Constructor")
        self.menu_bar_widget = MenuBarWidget(self)
        self.setMenuWidget(self.menu_bar_widget)

    def exec(self, app: QApplication) -> int:
        self.profiler.enable()
        result = app.exec()
        self.profiler.disable()
        self.profiler.write_profiling_stats_to_file("profiling_output.txt", os.getcwd())
        return result

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        super().closeEvent(event)
        QApplication.instance().installEventFilter(self)
