from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame

from PyQt6.QtGui import QPalette, QColor



class Init_Layout():
    def __init__(self, main_widget, main_window):
        self.main_widget = main_widget
        self.main_window = main_window
        self.init_layouts()
        self.configure_layouts()
        self.add_black_border_to_widgets()
        self.assign_layouts_to_window()
    
        
    def init_layouts(self):
        # Initialize all layouts and store them in a dictionary for easy access and management.
        self.layouts = {
            'main': QHBoxLayout(),
            'left': QVBoxLayout(),
            'right': QVBoxLayout(),
            'editor': QHBoxLayout(),
            'sequence': QVBoxLayout(),
            'objectbox': QVBoxLayout(),
            'graphboard': QVBoxLayout(),
            'action_buttons': QVBoxLayout(),
            'info': QVBoxLayout(),
            'word': QHBoxLayout(),
            'graphboard_and_buttons': QHBoxLayout(),
            'action_buttons': QVBoxLayout(),
            'optionboard': QHBoxLayout(),
            'letter_buttons': QVBoxLayout()
        }

    def configure_layouts(self):
        # Configure the hierarchy and properties of layouts.
        self.layouts['graphboard_and_buttons'].addLayout(self.layouts['graphboard'])
        self.layouts['graphboard_and_buttons'].addLayout(self.main_window.action_buttons_layout)
        self.layouts['graphboard_and_buttons'].setStretchFactor(self.layouts['graphboard'], 3)
        self.layouts['graphboard_and_buttons'].setStretchFactor(self.layouts['action_buttons'], 1)

        self.layouts['editor'].addLayout(self.layouts['objectbox'])
        self.layouts['editor'].addLayout(self.layouts['graphboard_and_buttons'])
        self.layouts['editor'].addLayout(self.layouts['info'])
        
        self.layouts['left'].addLayout(self.layouts['sequence'])
        self.layouts['left'].addLayout(self.layouts['editor'])
        self.layouts['main'].addLayout(self.layouts['left'])
        
        self.layouts['right'].addLayout(self.layouts['optionboard'])
        self.layouts['main'].addLayout(self.layouts['right'])
        
        self.layouts['graphboard'].addWidget(self.main_widget.graphboard_view)
        
        self.layouts['objectbox'].addWidget(self.main_widget.arrowbox_view.arrowbox_frame)
        self.layouts['objectbox'].addWidget(self.main_widget.propbox_view.propbox_frame)

        self.layouts['optionboard'].addWidget(self.main_widget.optionboard_view)

        self.layouts['action_buttons'].addLayout(self.layouts['action_buttons'])
        self.layouts['sequence'].addWidget(self.main_widget.word_label)
        self.layouts['sequence'].addWidget(self.main_widget.sequence_view)        
        self.layouts['sequence'].addWidget(self.main_widget.clear_sequence_button)        
        
        self.layouts['editor'].addLayout(self.main_window.letter_buttons_layout)
        self.layouts['info'].addWidget(self.main_widget.info_tracker.info_label)   
        
        self.main_widget.setLayout(self.layouts['main'])
        

    def add_black_border_to_widgets(self):
        self.add_black_border(self.main_widget.graphboard_view)
        self.add_black_border(self.main_widget.arrowbox_view.arrowbox_frame)
        self.add_black_border(self.main_widget.propbox_view.propbox_frame)
        self.add_black_border(self.main_widget.sequence_view)
        self.add_black_border(self.main_widget.word_label)
        self.add_black_border(self.main_widget.info_tracker.info_label)
        

    def assign_layouts_to_window(self):
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)
            
        
    def add_black_border(self, widget):
        widget.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        widget.setLineWidth(1)
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))  # Change "black" to any color you prefer for the border
        widget.setPalette(palette)

