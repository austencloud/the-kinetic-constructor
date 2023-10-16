from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

class Init_Layout():
    def __init__(self, ui_setup, main_window):
        self.ui_setup = ui_setup
        self.main_window = main_window
        self.init_layouts()
        self.configure_layouts()
        self.assign_layouts_to_window()

    def init_layouts(self):
        # Initialize all layouts and store them in a dictionary for easy access and management.
        self.layouts = {
            'main': QHBoxLayout(),
            'right': QVBoxLayout(),
            'upper': QHBoxLayout(),
            'lower': QVBoxLayout(),
            'objectbox': QVBoxLayout(),
            'graphboard': QVBoxLayout(),
            'button': QHBoxLayout(),
            'info': QVBoxLayout(),
            'word': QHBoxLayout(),
            'graphboard_with_button_panel': QHBoxLayout(),
        }

    def configure_layouts(self):
        # Configure the hierarchy and properties of layouts.
        self.layouts['graphboard_with_button_panel'].addLayout(self.layouts['graphboard'])
        self.layouts['graphboard_with_button_panel'].addLayout(self.layouts['button'])
        self.layouts['graphboard_with_button_panel'].setStretch(0, 1)

        self.layouts['upper'].addLayout(self.layouts['objectbox'])
        self.layouts['upper'].addLayout(self.layouts['graphboard_with_button_panel'])
        self.layouts['upper'].addLayout(self.layouts['info'])
        
        self.layouts['right'].addLayout(self.layouts['lower'])
        self.layouts['right'].addLayout(self.layouts['upper'])


        self.layouts['main'].addLayout(self.layouts['right'])

        self.main_window.setLayout(self.layouts['main'])
        self.layouts['graphboard'].addWidget(self.ui_setup.graphboard_view)

    def assign_layouts_to_window(self):
        # Assign layouts to the main window properties.
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)
