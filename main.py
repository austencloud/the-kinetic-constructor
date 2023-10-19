import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QScreen
from main_widget import Main_Widget
from settings import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.screen = QApplication.primaryScreen().geometry()
        self.init_main_window()
        self.initUI()
        
    def init_main_window(self):
        self.setMinimumSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.main_widget = Main_Widget(self)
        self.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Sequence Generator")

    def initUI(self):
        self.move(-(self.screen.width() + 500), 100)
 
    
app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec())
