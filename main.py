import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ui_setup import UiSetup

class Main_Window(QWidget):
    def __init__(self):
        super().__init__() 
        UiSetup(self)

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())
