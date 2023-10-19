from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt, QEvent
from objects.grid import Grid
from managers.arrow_manager import Arrow_Manager
from managers.staff_manager import Staff_Manager
from managers.svg_manager import Svg_Manager
from managers.json_manager import Json_Manager
from views.graphboard_view import Graphboard_View
from views.arrowbox_view import ArrowBox_View
from views.sequence_view import Sequence_View
from generator import Pictograph_Generator
from info_tracker import Info_Tracker
from exporter import Exporter
from pictograph_selector import Pictograph_Selector
from init.init_letter_buttons import Init_Letter_Buttons
from init.init_action_buttons import Init_Action_Buttons
from init.init_layout import Init_Layout
from init.key_bindings import Key_Bindings
from views.propbox_view import PropBox_View

class Main_Widget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.arrows = []
        self.main_widget = self
        self.exporter = None
        self.sequence_manager = None
        self.graphboard_view = None
        self.main_window = main_window
        self.key_bindings = Key_Bindings()
        self.json_manager = Json_Manager()
        self.letters = self.json_manager.load_all_letters()
        self.svg_manager = Svg_Manager()
        self.arrow_manager = Arrow_Manager(self)

        self.grid = Grid('images\\grid\\grid.svg')
        self.graphboard_view = Graphboard_View(self.grid, self.svg_manager, self.arrow_manager, self, None, self.sequence_manager, self.exporter, self.json_manager)
        self.staff_manager = Staff_Manager(self)
        self.exporter = Exporter(self.graphboard_view, self.staff_manager, self.grid)
        self.info_tracker = Info_Tracker(self)
        self.propbox_view = PropBox_View(self)
        self.arrowbox_view = ArrowBox_View(self)
        self.generator = Pictograph_Generator(self)
        
        self.arrow_manager.connect_to_graphboard(self.graphboard_view)
        self.info_tracker.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_info_tracker(self.info_tracker)
        self.staff_manager.connect_grid(self.grid)
        self.staff_manager.connect_graphboard_view(self.graphboard_view)
        self.staff_manager.connect_propbox_view(self.propbox_view)
        self.staff_manager.init_graphboard_staffs(self.graphboard_view)
        self.staff_manager.init_propbox_staffs(self.propbox_scene)
        
        self.graphboard_view.connect_info_tracker(self.info_tracker)
        self.graphboard_view.connect_staff_manager(self.staff_manager)

        Init_Layout(self, self.main_window)
        Init_Action_Buttons(self)
        self.connect_info_tracker()
        self.sequence_view = Sequence_View(self)
        Init_Letter_Buttons(self, self.main_window)

        self.setFocus()

        self.arrow_manager.connect_info_tracker(self.info_tracker)
        self.graphboard_view.connect_generator(self.generator)
        self.main_window.installEventFilter(self)

### CONNECTORS ###

    def connect_info_tracker(self):
        self.main_window.info_layout.addWidget(self.info_tracker.info_label)

### EVENTS ###

    def show_pictograph_selector(self, letter):
        combinations = self.generator.letters.get(letter, [])
        
        if not combinations:
            print(f"No combinations found for letter {letter}")
            return
        
        # Create and show the Pictograph_Selector pictograph_selector
        pictograph_selector = Pictograph_Selector(combinations, letter, self)
        result = pictograph_selector.exec()
        
        if result == QDialog.accepted:
            # TODO: Handle the selected pictograph
            pass


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:  # Adjusted to the new enumeration access method
            self.key_bindings.keyPressEvent(event, self.graphboard_view)
            return True
        return super().eventFilter(source, event)
