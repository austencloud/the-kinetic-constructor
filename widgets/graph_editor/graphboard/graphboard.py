from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsScene
from objects.arrow.arrow import Arrow, BlankArrow
from objects.staff.staff import Staff
from objects.grid import Grid
from settings.numerical_constants import STAFF_LENGTH, STAFF_WIDTH, LETTER_ITEM_HEIGHT
from settings.string_constants import (
    VERTICAL,
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
)
from data.letter_types import letter_types
from data.positions_map import positions_map
from .graphboard_init import GraphboardInit
from .graphboard_menu_handler import GraphboardMenuHandler
from .position_engines.staff_positioner import StaffPositioner
from .position_engines.arrow_positioner import ArrowPositioner
from objects.arrow.ghost_arrow import GhostArrow
from utilities.export_handler import ExportHandler
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
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
        self.current_letter = None

    def setup_components(self, main_widget, graph_editor):
        self.graph_editor = graph_editor
        self.letters = main_widget.letters
        self.letter_item = QGraphicsSvgItem()
        self.initializer = GraphboardInit(self)
        self.ghost_arrow = GhostArrow(self)

        self.grid = self.initializer.init_grid()
        self.view = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.setup_managers(main_widget, graph_editor)

    def setup_managers(self, main_widget, graph_editor):
        self.export_manager = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardMenuHandler(
            main_widget, graph_editor, self
        )
        self.arrow_positioner = ArrowPositioner(self)
        self.staff_positioner = StaffPositioner(self)
        self.letter_engine = LetterEngine(self)
        
    ### SELECTION

    def select_all_arrows(self):
        for arrow in self.arrows:
            arrow.setSelected(True)

    ### DELETION ###

    def clear_graphboard(self):
        for arrow in self.arrows:
            self.removeItem(arrow)
        for staff in self.staffs:
            staff.hide()

    def hide_all_staffs(self):
        for staff in self.staffs:
            staff.hide()

    def delete_arrow(self, arrow, keep_staff=False):
        self.removeItem(arrow)
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
        if isinstance(clicked_item, Grid):
            clicked_item = None
        if not clicked_item:
            self.clearSelection()
            event.accept()
        else:
            super().mousePressEvent(event)

    ### SETTERS ###

    def set_default_staff_locations(self, staff):
        if staff.axis == VERTICAL:
            staff.setPos(
                self.grid.handpoints[staff.location]
                + QPointF(self.padding, self.padding)
                + QPointF(STAFF_WIDTH / 2, -STAFF_LENGTH / 2)
            )
        else:
            staff.setPos(
                self.grid.handpoints[staff.location]
                + QPointF(self.padding, self.padding)
                + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2)
            )
        staff.setTransformOriginPoint(0, 0)

    def set_infobox(self, infobox):
        self.infobox = infobox

    def set_focus_and_accept_event(self, event):
        self.setFocus()
        event.accept()

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



    ### HELPERS ###

    @staticmethod
    def point_in_quadrant(x, y, boundary):
        return boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]

    def determine_quadrant(self, x, y):
        if self.point_in_quadrant(x, y, self.ne_boundary):
            return NORTHEAST
        elif self.point_in_quadrant(x, y, self.se_boundary):
            return SOUTHEAST
        elif self.point_in_quadrant(x, y, self.sw_boundary):
            return SOUTHWEST
        elif self.point_in_quadrant(x, y, self.nw_boundary):
            return NORTHWEST
        else:
            return None

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
        blank_arrow.is_still = True
        blank_arrow.staff = arrow.staff
        blank_arrow.staff.arrow = blank_arrow

    def center_letter_item(self):
        x = self.width() / 2 - self.letter_item.boundingRect().width() / 2
        y = self.grid.boundingRect().height() + LETTER_ITEM_HEIGHT
        self.letter_item.setPos(x, y)

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
        for staff in self.staffs:
            self.set_default_staff_locations(staff)

        if self.staff_positioner.staffs_in_beta():
            self.staff_positioner.reposition_beta_staffs()

    def update_letter(self):
        self.current_letter = self.letter_engine.get_current_letter() if len(self.staffs) == 2 else None
        self.update_letter_item(self.current_letter)

    def update_letter_item(self, letter):
        if letter:
            self.set_letter_renderer(letter)
        else:
            self.set_blank_renderer()

    ### SETTERS ###

    def set_letter_renderer(self, letter):
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        self.set_svg_renderer(svg_path)

    def set_blank_renderer(self):
        self.set_svg_renderer(f"{LETTER_SVG_DIR}/blank.svg")

    def set_svg_renderer(self, svg_path):
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)
            self.center_letter_item()
