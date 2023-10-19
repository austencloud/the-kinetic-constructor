from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QEvent
from objects.grid import Grid
from managers.arrow_manager import Arrow_Manager
from managers.staff_manager import Staff_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager
from views.graphboard_view import Graphboard_View
from views.arrowbox_view import ArrowBox_View
from views.sequence_view import Sequence_View
from views.optionboard_view import Optionboard_View
from pictograph_generator import Pictograph_Generator
from info_tracker import Info_Tracker
from exporter import Exporter
from pictograph_selector_dialog import Pictograph_Selector_Dialog
from init.letter_buttons import Letter_Buttons
from init.init_action_buttons import Action_Buttons
from init.init_layout import Init_Layout
from init.key_bindings import Key_Bindings
from views.propbox_view import PropBox_View

class Main_Widget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_widget = self
        self.arrows = []
        self.exporter = None
        self.main_window = main_window
        self.json_manager = Json_Manager()
        self.letters = self.json_manager.load_all_letters()
        self.grid = Grid('images/grid/grid.svg')
        self.staff_manager = Staff_Manager(self)
        self.key_bindings = Key_Bindings()
        self.svg_manager = Svg_Manager()
        self.arrow_manager = Arrow_Manager(self)
        self.graphboard_view = Graphboard_View(self)
        self.exporter = Exporter(self)
        self.info_tracker = Info_Tracker(self)
        self.propbox_view = PropBox_View(self)
        self.arrowbox_view = ArrowBox_View(self)
        self.pictograph_generator = Pictograph_Generator(self)
        self.sequence_view = Sequence_View(self)
        self.optionboard_view = Optionboard_View(self)
        self.pictograph_selector_dialog = Pictograph_Selector_Dialog(self)
        self.letter_buttons = Letter_Buttons(self, main_window)
        self.action_buttons = Action_Buttons(self)
        self.layout_initializer = Init_Layout(self, main_window)
        self.init_staffs()
        self.connect_objects()

    def init_staffs(self):
        self.staff_manager.init_graphboard_staffs(self.graphboard_view)
        self.staff_manager.init_propbox_staffs(self.propbox_view)

    def connect_objects(self):
        self.info_tracker.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_info_tracker(self.info_tracker)
        self.staff_manager.connect_grid(self.grid)
        self.staff_manager.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_propbox_view(self.propbox_view)
        self.graphboard_view.connect_info_tracker(self.info_tracker)
        self.graphboard_view.connect_staff_manager(self.staff_manager)
        self.graphboard_view.connect_generator(self.pictograph_generator)
        self.arrow_manager.connect_info_tracker(self.info_tracker)
        self.arrow_manager.connect_to_graphboard_view(self.graphboard_view)

### EVENTS ###


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            self.key_bindings.keyPressEvent(event, self.graphboard_view)
            return True
        return super().eventFilter(source, event)
