import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt


from .menu_bar_widget.menu_bar_widget import MenuBarWidget
from .settings_manager.settings_manager import SettingsManager
from .main_widget.main_widget import MainWidget
from profiler import Profiler
from main_window.main_window_geometry_manager import MainWindowGeometryManager

if TYPE_CHECKING:
    from splash_screen import SplashScreen


# In main_window.py
class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler, splash_screen: "SplashScreen") -> None:
        super().__init__()
        self.profiler = profiler
        self.main_widget = None  # Initialize main_widget to None
        self.settings_manager = SettingsManager(self)
        self.geometry_manager = MainWindowGeometryManager(self)
        self.main_widget = MainWidget(self, splash_screen)  # Set main_widget here
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("The Kinetic Constructor")
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
