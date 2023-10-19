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
            'right': QVBoxLayout(),
            'upper': QHBoxLayout(),
            'lower': QVBoxLayout(),
            'objectbox': QVBoxLayout(),
            'graphboard': QVBoxLayout(),
            'button': QVBoxLayout(),
            'info': QVBoxLayout(),
            'word': QHBoxLayout(),
            'graphboard_with_button_panel': QHBoxLayout(),
            'action_buttons': QVBoxLayout(),
            'optionboard': QHBoxLayout(),
            'letter_buttons': QVBoxLayout()
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
        self.layouts['main'].addLayout(self.layouts['optionboard'])
        
        self.layouts['graphboard'].addWidget(self.main_widget.graphboard_view)
        
        self.layouts['objectbox'].addWidget(self.main_widget.arrowbox_view.arrowbox_frame)
        self.layouts['objectbox'].addWidget(self.main_widget.propbox_view.propbox_frame)

        self.layouts['optionboard'].addWidget(self.main_widget.optionboard_view)

        self.layouts['button'].addLayout(self.layouts['action_buttons'])
        self.layouts['lower'].addWidget(self.main_widget.word_label)
        self.layouts['lower'].addWidget(self.main_widget.sequence_view)        
        self.layouts['lower'].addWidget(self.main_widget.clear_sequence_button)        
        
        self.layouts['upper'].addLayout(self.layouts['letter_buttons'])
        self.layouts['info'].addWidget(self.main_widget.info_tracker.info_label)   
        
        self.main_widget.setLayout(self.layouts['main'])
        

    def add_black_border_to_widgets(self):
        self.style_widget(self.main_widget.graphboard_view)
        self.style_widget(self.main_widget.arrowbox_view.arrowbox_frame)
        self.style_widget(self.main_widget.propbox_view.propbox_frame)
        self.style_widget(self.main_widget.sequence_view)
        self.style_widget(self.main_widget.word_label)
        self.style_widget(self.main_widget.info_tracker.info_label)
        

    def assign_layouts_to_window(self):
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)
            
        
    def style_widget(self, widget):
        widget.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        widget.setLineWidth(1)
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))  # Change "black" to any color you prefer for the border
        widget.setPalette(palette)
