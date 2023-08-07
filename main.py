import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from ui_setup import UiSetup

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Calculate the scaling factor
        base_width = 3840
        base_height = 2160
        screen_resolution = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        scale_factor_width = screen_width / base_width
        scale_factor_height = screen_height / base_height
        scale_factor = min(scale_factor_width, scale_factor_height)

        # Initialize the UI setup
        UiSetup(self)

        # Apply the scaling factor to the main window
        self.resize(int(self.width() * scale_factor), int(self.height() * scale_factor))

    def refresh_ui(self):
        self.close()  # Close the current window
        self.__init__()  # Reinitialize the main window
        self.show()  # Show the new window

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()
sys.exit(app.exec_())
