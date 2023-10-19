from PyQt6.QtWidgets import QWidget, QFrame
from views.graphboard_view import Graphboard_View
from views.arrowbox_view import ArrowBox_View
from pictograph_generator import Pictograph_Generator
from views.propbox_view import PropBox_View
from info_tracker import Info_Tracker
from exporter import Exporter

class Graph_Editor_Widget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.graph_editor_frame = QFrame()
        self.graphboard_view = Graphboard_View(main_widget)
        self.exporter = Exporter(main_widget.staff_manager, main_widget.grid, self.graphboard_view)
        self.info_tracker = Info_Tracker(main_widget, self.graphboard_view)
        self.propbox_view = PropBox_View(main_widget)
        self.arrowbox_view = ArrowBox_View(main_widget, self.graphboard_view, self.info_tracker)
        self.pictograph_generator = Pictograph_Generator(main_widget, self.graphboard_view, self.info_tracker)
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)