import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from init.ui_setup import UiSetup
from settings import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
class Main_Window(QWidget):
    def __init__(self):
        super().__init__() 
        self.init_main_window()
        self.ui_setup = UiSetup(self)
        self.initUI()

    def init_main_window(self):
        self.setMinimumSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.show()
        self.setWindowTitle("Sequence Generator")

    def initUI(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(-screen.width() + 900, 300)
        
app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())
