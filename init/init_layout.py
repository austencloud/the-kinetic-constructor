from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

class Init_Layout():
    def __init__(self, main_widget, main_window):
        self.main_widget = main_widget
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
        self.layouts['graphboard_with_button_panel'].setStretchFactor(self.layouts['graphboard'], 3)
        self.layouts['graphboard_with_button_panel'].setStretchFactor(self.layouts['button'], 1)

        self.layouts['upper'].addLayout(self.layouts['objectbox'])
        self.layouts['upper'].addLayout(self.layouts['graphboard_with_button_panel'])
        self.layouts['upper'].addLayout(self.layouts['info'])
        
        self.layouts['right'].addLayout(self.layouts['lower'])
        
        self.layouts['right'].addLayout(self.layouts['upper'])
        self.layouts['main'].addLayout(self.layouts['right'])

        self.main_widget.setLayout(self.layouts['main'])
        self.layouts['graphboard'].addWidget(self.main_widget.graphboard_view)
        
        self.layouts['objectbox'].addWidget(self.main_widget.arrowbox_view.arrowbox_frame)
        self.layouts['objectbox'].addWidget(self.main_widget.propbox_view.propbox_frame)

    def assign_layouts_to_window(self):
        # Assign layouts to the main window properties.
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)
