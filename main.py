import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from widgets.main_widget import MainWidget
from settings.numerical_constants import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen = QApplication.primaryScreen().geometry()
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

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()
sys.exit(app.exec())
