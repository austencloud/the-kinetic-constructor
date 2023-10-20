from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtGui import QPalette, QColor
from widgets.graph_editor_widget import Graph_Editor_Widget

class Layout_Manager():
    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.init_layouts()
        self.assign_layouts_to_window()


    def configure_layouts(self):
        self.configure_main_layout()
        self.init_sequence_layout()
        self.init_action_buttons_layout()
        self.init_letter_buttons_layout()
        self.add_black_border_to_widgets()
        
    def init_layouts(self):
        # Initialize all layouts and store them in a dictionary for easy access and management.
        self.layouts = {
            'main': QHBoxLayout(),
            'left': QVBoxLayout(),
            'right': QVBoxLayout(),
            'graph_editor': QHBoxLayout(),
            'sequence': QHBoxLayout(),
            'objectbox': QVBoxLayout(),
            'graphboard': QVBoxLayout(),
            'info': QVBoxLayout(),
            'word': QHBoxLayout(),
            'graphboard_and_buttons': QHBoxLayout(),
            'optionboard': QHBoxLayout(),
            'letter_buttons': QVBoxLayout(),
            'sequence_with_label_and_button': QVBoxLayout(),
            'keyboard': QVBoxLayout(),
        }

    def configure_main_layout(self):

        self.layouts['left'].addLayout(self.layouts['sequence'])
        self.layouts['left'].addLayout(self.layouts['graph_editor'])
        self.layouts['main'].addLayout(self.layouts['left'])
        
        self.layouts['right'].addLayout(self.layouts['optionboard'])
        self.layouts['main'].addLayout(self.layouts['right'])
        self.layouts['optionboard'].addWidget(self.main_widget.optionboard_view)
        
        self.main_widget.setLayout(self.layouts['main'])
        
        self.add_black_border_to_widgets()

    def init_sequence_layout(self):
        self.layouts['sequence_with_label_and_button'].addWidget(self.main_widget.word_label)
        self.layouts['sequence_with_label_and_button'].addWidget(self.main_widget.sequence_view)
        self.layouts['sequence_with_label_and_button'].addWidget(self.main_widget.clear_sequence_button)
        self.layouts['sequence'].addLayout(self.layouts['sequence_with_label_and_button'])
        
    def add_black_border_to_widgets(self):
        # Method to add black borders to specific widgets
        self.add_black_border(self.main_widget.graph_editor_widget.graphboard_view)
        self.add_black_border(self.main_widget.sequence_view)
        self.add_black_border(self.main_widget.word_label)
        self.add_black_border(self.main_widget.graph_editor_widget.info_manager.info_label)
        self.add_black_border(self.main_widget.optionboard_view)
        self.add_black_border(self.main_widget.graph_editor_widget.action_buttons_frame)
        self.add_black_border(self.main_widget.graph_editor_widget.letter_buttons_frame)
        self.add_black_border(self.main_widget.graph_editor_widget.graphboard_view)
        self.add_black_border(self.main_widget.graph_editor_widget.propbox_view)
        

    def assign_layouts_to_window(self):
        # Assign layouts to the main window for further configurations outside this class
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)

    def add_black_border(self, widget):
        # Check if 'widget' has the 'setFrameStyle' method
        if hasattr(widget, 'setFrameStyle'):
            widget.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            widget.setLineWidth(1)
            palette = widget.palette()
            palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
            widget.setPalette(palette)
        else:
            # Optionally, handle the case when 'setFrameStyle' is not available
            print(f"Widget {type(widget).__name__} does not support setFrameStyle.")

        
    def init_action_buttons_layout(self):
        self.main_window.graphboard_and_buttons_layout.addLayout(self.main_widget.graph_editor_widget.action_buttons_frame.action_buttons_layout)
        
    def init_letter_buttons_layout(self):
        self.main_window.sequence_layout.addLayout(self.main_widget.graph_editor_widget.letter_buttons_frame.letter_buttons_layout) 
