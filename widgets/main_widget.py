from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QEvent
from objects.grid import Grid
from managers.arrow_management.arrow_manager import ArrowManager
from managers.svg_manager import SvgManager
from managers.json_manager import JsonManager
from views.sequence_view import SequenceView
from views.optionboard_view import OptionboardView
from managers.layout_manager import LayoutManager
from managers.key_bindings_manager import KeyBindingsManager
from widgets.graph_editor_widget import GraphEditorWidget
from frames.letter_buttons_frame import LetterButtonsFrame

class MainWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_widget = self
        self.arrows = []
        self.export_manager = None
        self.main_window = main_window
        
        self.layout_manager = LayoutManager(self)
        self.json_manager = JsonManager()
        self.letters = self.json_manager.load_all_letters()
        self.key_bindings_manager = KeyBindingsManager()
        self.svg_manager = SvgManager()
        self.arrow_manager = ArrowManager(self)
        self.graph_editor_widget = GraphEditorWidget(self)  
        self.optionboard_view = OptionboardView(self)
        self.sequence_view = SequenceView(self)
        self.letter_buttons_frame = LetterButtonsFrame(self)  

        self.graphboard_view = self.graph_editor_widget.graphboard_view
        self.info_frame = self.graph_editor_widget.info_frame
        self.propbox_view = self.graph_editor_widget.propbox_view
        
        self.layout_manager.configure_layouts()
        self.init_staffs()
        self.connect_objects()

    def init_staffs(self):
        self.graphboard_view.staff_manager.init_graphboard_staffs(self.graph_editor_widget.graphboard_view)
        self.propbox_view.staff_manager.init_propbox_staffs(self.graph_editor_widget.propbox_view)

    def connect_objects(self):
        self.info_frame.connect_view(self.graph_editor_widget.graphboard_view)
        self.graphboard_view.staff_manager.info_manager = self.graphboard_view.info_manager
        self.graphboard_view.staff_manager.grid = self.graphboard_view.grid
        self.graphboard_view.staff_manager.graphboard_view = self.graph_editor_widget.graphboard_view
        self.propbox_view.staff_manager.propbox_view = self.graph_editor_widget.propbox_view
        self.graphboard_view.info_frame = self.graph_editor_widget.info_frame
        self.graphboard_view.generator = self.graph_editor_widget.pictograph_generator
        self.arrow_manager.info_frame = self.graph_editor_widget.info_frame
        self.arrow_manager.graphboard_view = self.graph_editor_widget.graphboard_view
        self.arrow_manager.arrow_manipulator.graphboard_scene = self.graph_editor_widget.graphboard_view.graphboard_scene
        self.graph_editor_widget.graphboard_view.context_menu_manager.sequence_view = self


### EVENTS ###


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            self.key_bindings_manager.keyPressEvent(event, self.graph_editor_widget.graphboard_view)
            return True
        return super().eventFilter(source, event)
