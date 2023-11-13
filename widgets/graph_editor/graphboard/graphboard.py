from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsScene
from objects.arrow import Arrow, BlankArrow
from objects.staff import Staff
from settings.string_constants import (
    ARROWS,
    COLOR,
    MOTION_TYPE,
    STATIC,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    RED,
    BLUE,
    LETTER_SVG_DIR,
    NORTHWEST,
    SOUTHWEST,
    SOUTHEAST,
    NORTHEAST,
    LOCATION,
    VERTICAL,
    HORIZONTAL,
)
from settings.numerical_constants import STAFF_WIDTH, STAFF_LENGTH
from data.letter_types import letter_types
from .graphboard_init import GraphboardInit
from .graphboard_menu_handler import GraphboardMenuHandler
from .position_engines.staff_positioner import StaffPositioner
from .position_engines.arrow_positioner import ArrowPositioner
from utilities.export_handler import ExportHandler
from utilities.letter_engine import LetterEngine


class Graphboard(QGraphicsScene):
    def __init__(self, main_widget, graph_editor):
        super().__init__()
        self.setup_scene()
        self.setup_components(main_widget, graph_editor)

    def setup_scene(self):
        self.setSceneRect(0, 0, 750, 900)
        self.arrows = []
        self.staffs = []
        self.letter_renderers = {}
        self.current_letter = None
        self.infobox = None

    def setup_components(self, main_widget, graph_editor):
        self.graph_editor = graph_editor
        self.letters = main_widget.letters

        self.dragged_arrow = None
        self.dragged_staff = None

        self.initializer = GraphboardInit(self)

        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.ghost_staffs = self.initializer.init_ghost_staffs()
        self.grid = self.initializer.init_grid()
        self.view = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.letter_item = self.initializer.init_letter_item()
        self.quadrants = self.initializer.init_quadrants(self.grid)
        self.setup_managers(main_widget, graph_editor)

    def setup_managers(self, main_widget, graph_editor):
        self.export_handler = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardMenuHandler(
            main_widget, graph_editor, self
        )
        self.arrow_positioner = ArrowPositioner(self)
        self.staff_positioner = StaffPositioner(self)
        self.letter_engine = LetterEngine(self)

    ### DELETION ###

    def delete_arrow(self, arrow, keep_staff=False):
        self.removeItem(arrow)
        if arrow in self.arrows:
            self.arrows.remove(arrow)
        if keep_staff:
            self.create_blank_arrow(arrow)
        else:
            self.delete_staff(arrow.staff)

        self.update()

    def delete_staff(self, staff):
        self.removeItem(staff)
        self.staffs.remove(staff)
        self.update()

    ### EVENTS ###

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(
            self.view.mapToScene(event.pos().toPoint().x(), event.pos().toPoint().y()),
            QTransform(),
        )
        selected_items = self.selectedItems()
        event_pos = event.screenPos()

        if isinstance(clicked_item, Arrow):
            self.context_menu_manager.create_arrow_menu(selected_items, event_pos)
        elif isinstance(clicked_item, Staff):
            self.context_menu_manager.create_staff_menu(selected_items, event_pos)
        else:
            self.context_menu_manager.create_graphboard_menu(event_pos)

    def mousePressEvent(self, event):
        clicked_item = self.itemAt(event.scenePos(), QTransform())
        if isinstance(clicked_item, Staff):
            self.dragged_staff = clicked_item
            self.dragged_staff.mousePressEvent(
                event
            )  # Pass the event to the Staff class
        elif isinstance(clicked_item, Arrow):
            self.dragged_arrow = clicked_item
            self.dragged_arrow.mousePressEvent(event)
        else:
            self.dragged_staff = None
            self.dragged_arrow = None

    def mouseMoveEvent(self, event):
        if self.dragged_staff:
            # Delegate to Staff class
            self.dragged_staff.mouseMoveEvent(
                event
            )  # Pass the event to the Staff class
        elif self.dragged_arrow:
            self.dragged_arrow.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragged_staff:
            # Delegate to Staff class
            self.dragged_staff.mouseReleaseEvent(
                event
            )  # Pass the event to the Staff class
            self.dragged_staff = None
        elif self.dragged_arrow:
            self.dragged_arrow.mouseReleaseEvent(event)
            self.dragged_arrow = None

    ### GETTERS ###

    def get_current_arrow_coordinates(self):
        """Returns the coordinates for setting optimal positions"""
        red_position = None
        blue_position = None

        for arrow in self.arrows:
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position

    def get_state(self):
        state = {
            ARROWS: [],
        }
        for arrow in self.arrows:
            state[ARROWS].append(
                {
                    COLOR: arrow.color,
                    MOTION_TYPE: arrow.motion_type,
                    ROTATION_DIRECTION: arrow.rotation_direction,
                    QUADRANT: arrow.quadrant,
                    START_LOCATION: arrow.start_location,
                    END_LOCATION: arrow.end_location,
                    TURNS: arrow.turns,
                }
            )
        return state

    def get_current_letter_type(self):
        if self.current_letter is not None:
            for letter_type, letters in letter_types.items():
                if self.current_letter in letters:
                    return letter_type
        else:
            return None

    def get_arrow_by_color(self, color):
        for arrow in self.arrows:
            if arrow.color == color:
                return arrow

    def get_quadrant(self, x, y):
        if self.point_in_quadrant(x, y, self.quadrants[NORTHEAST]):
            return NORTHEAST
        elif self.point_in_quadrant(x, y, self.quadrants[SOUTHEAST]):
            return SOUTHEAST
        elif self.point_in_quadrant(x, y, self.quadrants[SOUTHWEST]):
            return SOUTHWEST
        elif self.point_in_quadrant(x, y, self.quadrants[NORTHWEST]):
            return NORTHWEST
        else:
            return None

    ### MANIPULATORS ###

    def swap_colors(self):
        if self.current_letter != "G" and self.current_letter != "H":
            if len(self.arrows) >= 1:
                for arrow in self.arrows:
                    if arrow.color == RED:
                        new_color = BLUE
                    elif arrow.color == BLUE:
                        new_color = RED
                    else:
                        continue
                    arrow.color = new_color
                    arrow.staff.color = new_color
                    arrow.update_appearance()
                    arrow.staff.update_appearance()

                self.update()

    ### HELPERS ###

    @staticmethod
    def point_in_quadrant(x, y, boundary):
        return boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]

    def create_blank_arrow(self, arrow):
        deleted_arrow_attributes = arrow.attributes
        blank_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow_attributes[END_LOCATION],
            END_LOCATION: deleted_arrow_attributes[END_LOCATION],
            TURNS: 0,
        }
        blank_arrow = BlankArrow(self, blank_attributes_dict)
        self.addItem(blank_arrow)
        self.arrows.append(blank_arrow)
        blank_arrow.staff = arrow.staff
        blank_arrow.staff.arrow = blank_arrow


    ### UPDATERS ###

    def update(self):
        self.update_letter()
        self.update_arrows()
        self.update_staffs()
        self.update_infobox()

    def update_infobox(self):
        self.infobox.update()

    def update_arrows(self):
        self.arrow_positioner.update()

    def update_staffs(self):
        self.staff_positioner.update()

    def update_letter(self):
        if len(self.staffs) == 2:
            self.current_letter = self.letter_engine.get_current_letter()
        else:
            self.current_letter = None
        self.update_letter_item(self.current_letter)

    def update_letter_item(self, letter):
        if letter:
            self.set_letter_renderer(letter)
        else:
            self.letter_item.setSharedRenderer(QSvgRenderer(f"{LETTER_SVG_DIR}/blank.svg"))

    ### SETTERS ###

    def set_letter_renderer(self, letter):
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)
    
