import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from ui_setup import UiSetup

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()


        # Initialize the UI setup
        UiSetup(self)

    def refresh_ui(self):
        self.close()  # Close the current window
        self.__init__()  # Reinitialize the main window
        self.show()  # Show the new window

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()
sys.exit(app.exec_())
