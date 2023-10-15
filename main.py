import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from init.ui_setup import UiSetup

class Main_Window(QWidget):
    def __init__(self):
        super().__init__() 
        UiSetup(self)
        self.initUI()

    def initUI(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(-screen.width() + 900, 300)
        
app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())
