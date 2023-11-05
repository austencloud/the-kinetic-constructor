from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from widgets.graph_editor.graphboard.graphboard_view import GraphboardView
from widgets.graph_editor.arrowbox.arrowbox_view import ArrowBoxView

from widgets.graph_editor.propbox.propbox_view import PropBoxView
from widgets.graph_editor.infobox.infobox import InfoboxFrame
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from widgets.graph_editor.action_buttons_frame import ActionButtonsFrame


class GraphEditorWidget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.json_handler = main_widget.json_handler
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator
        self.arrow_selector = self.arrow_manager.selector
        self.arrow_attributes = self.arrow_manager.attributes
        self.sequence_view = main_widget.sequence_view
        self.graph_editor_frame = QFrame()
        self.graph_editor_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.graph_editor_frame.setLineWidth(1)
        palette = self.graph_editor_frame.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.graph_editor_frame.setPalette(palette)

        graph_editor_frame_layout = QHBoxLayout(self.graph_editor_frame)
        
        objectbox_layout = QVBoxLayout()
        graphboard_layout = QVBoxLayout()
        action_buttons_layout = QVBoxLayout()
        infobox_layout = QVBoxLayout()

        self.graphboard_view = GraphboardView(main_widget, self)
        self.infobox = InfoboxFrame(main_widget, self.graphboard_view, self.arrow_manipulator, self.arrow_attributes)
        self.infobox.init_manager()
        self.propbox_view = PropBoxView(main_widget)
        self.arrowbox_view = ArrowBoxView(
            main_widget,
            self.graphboard_view,
            self.infobox,
            self.arrow_manager,
        )
        self.action_buttons_frame = ActionButtonsFrame(self.graphboard_view, self.json_handler, self.arrow_manipulator, self.arrow_selector, self.sequence_view)

        objectbox_layout.addWidget(self.arrowbox_view)
        objectbox_layout.addWidget(self.propbox_view)
        graphboard_layout.addWidget(self.graphboard_view)
        action_buttons_layout.addWidget(self.action_buttons_frame) 
        infobox_layout.addWidget(self.infobox)

        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(action_buttons_layout)
        graph_editor_frame_layout.addLayout(infobox_layout)

        self.graph_editor_frame.setLayout(graph_editor_frame_layout)
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        global dragged_arrow
        if dragged_arrow:
            self.arrowbox_view.drag_manager.update_drag_preview(
                self.arrowbox_view, event
            )
