from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QEvent
from objects.grid import Grid
from managers.arrow_manager import Arrow_Manager
from managers.staff_manager import Staff_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager
from views.sequence_view import Sequence_View
from views.optionboard_view import Optionboard_View
from managers.layout_manager import Layout_Manager
from key_bindings import Key_Bindings
from graph_editor_widget import Graph_Editor_Widget
class Main_Widget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_widget = self
        self.arrows = []
        self.exporter = None
        self.main_window = main_window
        self.layout_manager = Layout_Manager(self)
        self.json_manager = Json_Manager()
        self.letters = self.json_manager.load_all_letters()
        self.grid = Grid('images/grid/grid.svg')
        self.staff_manager = Staff_Manager(self)
        self.key_bindings = Key_Bindings()
        self.svg_manager = Svg_Manager()
        self.arrow_manager = Arrow_Manager(self)
        
        self.graph_editor_widget = Graph_Editor_Widget(self)      


        
        
        self.optionboard_view = Optionboard_View(self)
        self.sequence_view = Sequence_View(self)
        self.layout_manager.configure_layouts()
        self.init_staffs()
        self.connect_objects()

    def init_staffs(self):
        self.staff_manager.init_graphboard_staffs(self.graph_editor_widget.graphboard_view)
        self.staff_manager.init_propbox_staffs(self.graph_editor_widget.propbox_view)

    def connect_objects(self):
        self.graph_editor_widget.info_tracker.connect_graphboard_view(self.graph_editor_widget.graphboard_view)
        self.staff_manager.connect_info_tracker(self.graph_editor_widget.info_tracker)
        self.staff_manager.connect_grid(self.grid)
        self.staff_manager.connect_graphboard_view(self.graph_editor_widget.graphboard_view)
        self.staff_manager.connect_propbox_view(self.graph_editor_widget.propbox_view)
        self.graph_editor_widget.graphboard_view.connect_info_tracker(self.graph_editor_widget.info_tracker)
        self.graph_editor_widget.graphboard_view.connect_staff_manager(self.staff_manager)
        self.graph_editor_widget.graphboard_view.connect_generator(self.graph_editor_widget.pictograph_generator)
        self.arrow_manager.connect_info_tracker(self.graph_editor_widget.info_tracker)
        self.arrow_manager.connect_to_graphboard_view(self.graph_editor_widget.graphboard_view)

### EVENTS ###


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            self.key_bindings.keyPressEvent(event, self.graph_editor_widget.graphboard_view)
            return True
        return super().eventFilter(source, event)
