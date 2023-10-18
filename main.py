import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QScreen
from main_widget import Main_Widget
from settings import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.init_main_window()
        self.initUI()
        
    def init_main_window(self):
        self.main_widget = Main_Widget(self)
        self.setCentralWidget(self.main_widget)
        self.setMinimumSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.show()
        self.setWindowTitle("Sequence Generator")

    def initUI(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(-screen.width() + 900, 0)
        
app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec())
