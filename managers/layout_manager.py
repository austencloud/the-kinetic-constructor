from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtGui import QPalette, QColor
from graph_editor_widget import Graph_Editor_Widget

class Layout_Manager():
    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.init_layouts()
        self.assign_layouts_to_window()


    def configure_layouts(self):
        self.configure_main_layout()
        self.init_sequence_layout()
        self.init_graph_editor_layout()
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
            'sequence': QVBoxLayout(),
            'objectbox': QVBoxLayout(),
            'graphboard': QVBoxLayout(),
            'action_buttons': QVBoxLayout(),
            'info': QVBoxLayout(),
            'word': QHBoxLayout(),
            'graphboard_and_buttons': QHBoxLayout(),
            'optionboard': QHBoxLayout(),
            'letter_buttons': QVBoxLayout()
        }

    def configure_main_layout(self):


        self.layouts['left'].addLayout(self.layouts['sequence'])
        self.layouts['left'].addLayout(self.layouts['graph_editor'])
        self.layouts['main'].addLayout(self.layouts['left'])
        
        self.layouts['right'].addLayout(self.layouts['optionboard'])
        self.layouts['main'].addLayout(self.layouts['right'])

        self.layouts['graphboard'].addWidget(self.main_widget.graph_editor_widget.graphboard_view)
        self.layouts['optionboard'].addWidget(self.main_widget.optionboard_view)

        self.main_widget.setLayout(self.layouts['main'])
        
        self.add_black_border_to_widgets()

    def init_sequence_layout(self):
        self.layouts['sequence'].addWidget(self.main_widget.word_label)
        self.layouts['sequence'].addWidget(self.main_widget.sequence_view)
        self.layouts['sequence'].addWidget(self.main_widget.clear_sequence_button)

    def add_black_border_to_widgets(self):
        # Method to add black borders to specific widgets
        self.add_black_border(self.main_widget.graph_editor_widget.graphboard_view)
        self.add_black_border(self.main_widget.graph_editor_widget.arrowbox_view.arrowbox_frame)
        self.add_black_border(self.main_widget.graph_editor_widget.propbox_view.propbox_frame)
        self.add_black_border(self.main_widget.sequence_view)
        self.add_black_border(self.main_widget.word_label)
        self.add_black_border(self.main_widget.graph_editor_widget.info_tracker.info_label)
        self.add_black_border(self.main_widget.optionboard_view)
        self.add_black_border(self.main_widget.graph_editor_widget.graph_editor_frame)

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

    def init_graph_editor_layout(self):
        self.main_window.graphboard_and_buttons_layout.addLayout(self.main_window.graphboard_layout)
        self.main_window.graphboard_and_buttons_layout.addLayout(self.main_window.action_buttons_layout)
        self.main_window.graphboard_and_buttons_layout.setStretchFactor(self.main_window.graphboard_layout, 3)
        self.main_window.graphboard_and_buttons_layout.setStretchFactor(self.main_window.action_buttons_layout, 1)
        
        self.main_window.objectbox_layout.addWidget(self.main_widget.graph_editor_widget.arrowbox_view.arrowbox_frame)
        self.main_window.objectbox_layout.addWidget(self.main_widget.graph_editor_widget.propbox_view.propbox_frame)
        self.main_window.info_layout.addWidget(self.main_widget.graph_editor_widget.info_tracker.info_label)

        self.main_window.graph_editor_layout.addLayout(self.main_window.objectbox_layout)
        self.main_window.graph_editor_layout.addLayout(self.main_window.graphboard_and_buttons_layout)
        self.main_window.graph_editor_layout.addLayout(self.main_window.info_layout)
        self.main_window.graph_editor_layout.addLayout(self.main_window.letter_buttons_layout)
        
        self.main_widget.graph_editor_widget.setLayout(self.main_window.graph_editor_layout)
        
    def init_action_buttons_layout(self):
        self.main_window.graphboard_and_buttons_layout.addLayout(self.main_widget.action_buttons.action_buttons_layout)
        
    def init_letter_buttons_layout(self):
        self.main_window.graph_editor_layout.addLayout(self.main_widget.letter_buttons.letter_buttons_layout)