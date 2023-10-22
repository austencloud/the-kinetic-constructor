from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from views.graphboard_view import Graphboard_View
from views.arrowbox_view import ArrowBox_View
from tools.pictograph_generator import Pictograph_Generator
from views.propbox_view import PropBox_View
from frames.graphboard_info_frame import Graphboard_Info_Frame
from managers.export_manager import Export_Manager
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from frames.action_buttons_frame import Action_Buttons_Frame
class Graph_Editor_Widget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window

        # Create the frame and set its style
        self.graph_editor_frame = QFrame()
        self.graph_editor_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.graph_editor_frame.setLineWidth(1)
        palette = self.graph_editor_frame.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.graph_editor_frame.setPalette(palette)

        # Create a main horizontal layout for the graph_editor_frame
        graph_editor_frame_layout = QHBoxLayout(self.graph_editor_frame)

        # Create individual vertical layouts
        objectbox_layout = QVBoxLayout()  # For arrowbox and propbox
        graphboard_layout = QVBoxLayout()  # For the graph board view
        action_buttons_layout = QVBoxLayout()  # For action buttons
        info_frame_layout = QVBoxLayout()  # For the info frame
        
        # Create and add contents to the graph_editor_frame_layout
        self.graphboard_view = Graphboard_View(main_widget, self)
        self.export_manager = Export_Manager(self.graphboard_view.staff_manager, main_widget.grid, self.graphboard_view)
        self.info_frame = Graphboard_Info_Frame(main_widget, self.graphboard_view)
        self.propbox_view = PropBox_View(main_widget)
        self.arrowbox_view = ArrowBox_View(main_widget, self.graphboard_view, self.info_frame)
        self.pictograph_generator = Pictograph_Generator(main_widget, self.graphboard_view, self.info_frame)
        self.action_buttons_frame = Action_Buttons_Frame(main_widget)
        
        # Add widgets to the object box layout.
        objectbox_layout.addWidget(self.arrowbox_view)
        objectbox_layout.addWidget(self.propbox_view)

        # Add the graph board view to its layout
        graphboard_layout.addWidget(self.graphboard_view)

        # Add the action buttons frame to its layout
        action_buttons_layout.addWidget(self.action_buttons_frame)  # self.action_buttons_frame is an instance of Action_Buttons_Frameself.

        # Add the info frame to its layout
        info_frame_layout.addWidget(self.info_frame)

        # Add the individual vertical layouts to the main horizontal layout
        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(action_buttons_layout)
        graph_editor_frame_layout.addLayout(info_frame_layout)

        self.graph_editor_frame.setLayout(graph_editor_frame_layout)  # This line is crucial.
        
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)

