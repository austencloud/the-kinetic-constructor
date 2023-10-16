from settings import GRAPHBOARD_SCALE

class Init_Main_Window:
    def __init__(self, ui_setup, main_window):
        self.init_main_window(ui_setup, main_window)
    
    def init_main_window(self, ui_setup, main_window):
        main_window.installEventFilter(ui_setup)
        main_window.setMinimumSize(int(2000 * GRAPHBOARD_SCALE), int(2000 * GRAPHBOARD_SCALE))
        main_window.show()
        main_window.setWindowTitle("Sequence Generator")
        