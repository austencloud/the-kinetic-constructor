from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from widgets.graph_editor.graphboard.graphboard_view import GraphboardView
from widgets.graph_editor.arrowbox.arrowbox_view import ArrowBoxView

from widgets.graph_editor.propbox.propbox_view import PropBoxView
from widgets.graph_editor.info_frame import InfoFrame
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from widgets.graph_editor.action_buttons_frame import ActionButtonsFrame

class GraphEditorWidget(QWidget):
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
        objectbox_layout = QVBoxLayout() 
        graphboard_layout = QVBoxLayout()  
        action_buttons_layout = QVBoxLayout()  
        info_frame_layout = QVBoxLayout() 
        
        # Create and add contents to the graph_editor_frame_layout
        self.graphboard_view = GraphboardView(main_widget, self)
        self.info_frame = InfoFrame(main_widget, self.graphboard_view)
        self.propbox_view = PropBoxView(main_widget)
        self.arrowbox_view = ArrowBoxView(main_widget, self.graphboard_view, self.info_frame, self.main_widget.arrow_manager)
        self.action_buttons_frame = ActionButtonsFrame(main_widget)
        
        # Add widgets to their layouts
        objectbox_layout.addWidget(self.arrowbox_view)
        objectbox_layout.addWidget(self.propbox_view)
        graphboard_layout.addWidget(self.graphboard_view)
        action_buttons_layout.addWidget(self.action_buttons_frame)  # self.action_buttons_frame is an instance of Action_Buttons_Frameself.
        info_frame_layout.addWidget(self.info_frame)

        # Add the individual vertical layouts to the main horizontal layout
        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(action_buttons_layout)
        graph_editor_frame_layout.addLayout(info_frame_layout)

        # Add the graph_editor_frame to the main_window's graph_editor_layout
        self.graph_editor_frame.setLayout(graph_editor_frame_layout)
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)

        self.setMouseTracking(True)  # Enable mouse tracking

    def mouseMoveEvent(self, event):
        global dragged_arrow
        if dragged_arrow:
            # Update the drag preview position based on global mouse position
            self.arrowbox_view.mouse_events.update_drag_preview(self.arrowbox_view, event)