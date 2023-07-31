import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ui_setup import UiSetup

class Main_Window(QWidget):
    def __init__(self):
        super().__init__() 
        self.ui_setup = UiSetup(self)
        self.ui_setup.initStaffManager()
        self.ui_setup.initLayouts()
        self.ui_setup.initInfoTracker()
        self.ui_setup.initArtboard()
        self.ui_setup.connectArtboard()
        self.ui_setup.initHandlers()
        self.ui_setup.initLetterButtons()
        self.ui_setup.initArrowBox()
        self.ui_setup.initGenerator()
        self.ui_setup.initPropBox()
        self.ui_setup.initButtons()
        self.ui_setup.connectInfoTracker()
        self.ui_setup.initWordLabel()
        self.ui_setup.initSequenceScene()
        self.ui_setup.setFocus()

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())
