from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsScene
from objects.arrow.arrow import Arrow, BlankArrow
from objects.staff.staff import Staff
from objects.grid import Grid
from settings.numerical_constants import *
from settings.string_constants import *
from data.letter_types import letter_types
from data.positions_map import positions_map
from widgets.graph_editor.graphboard.graphboard_init import GraphboardInit
from widgets.graph_editor.graphboard.position_optimizers.staff_positioner import (
    StaffPositioner,
)
from widgets.graph_editor.graphboard.position_optimizers.arrow_positioner import (
    ArrowPositioner,
)
from widgets.graph_editor.graphboard.graphboard_menu_handler import (
    GraphboardMenuHandler,
)
from utilities.export_handler import ExportHandler
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


class Graphboard(QGraphicsScene):
    def __init__(self, graph_editor, letters):
        super().__init__()
        self.graph_editor = graph_editor

        self.setSceneRect(0, 0, 750, 900)
        self.arrows = []
        self.staffs = []
        self.current_letter = None

        self.letters = letters
        self.letter_item = QGraphicsSvgItem()

        self.initializer = GraphboardInit(self)
        self.grid = self.initializer.init_grid()
        self.view = self.initializer.init_view()
        self.staff_set = self.initializer.init_staff_set()
        self.staffs = []

        self.export_manager = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardMenuHandler(
            graph_editor.main_widget, graph_editor, self
        )
        self.arrow_positioner = ArrowPositioner(self)
        self.staff_positioner = StaffPositioner(self)

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
            self.create_ghost_arrow(arrow)
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

    def get_current_letter(self):
        start_locations, end_locations = self.get_start_end_locations()
        # Generate the representation of current state with arrow attributes
        current_combination = self.get_state()[ARROWS]
        specific_position = {
            "start_position": positions_map.get(start_locations),
            "end_position": positions_map.get(end_locations),
        }

        # Ensure we have valid start and end positions
        if specific_position["start_position"] and specific_position["end_position"]:
            overall_position = self.get_overall_position(specific_position)
            possible_letters = self.get_possible_letters(overall_position)

            # Now, check through the possible letters to find a match
            for letter, combinations in possible_letters.items():
                # Check each combination in the possible letters
                for combination in combinations:
                    if self.match_combination(current_combination, combination):
                        self.letter = letter
                        return letter  # Once a match is found, return immediately
        return None  # In case of no match

    def get_overall_position(self, specific_positions):
        # Refactoring as per previous recommendation
        return {position: value[:-1] for position, value in specific_positions.items()}

    def get_possible_letters(self, overall_position):
        category_map = {
            "alpha": "ABCDEFWXα",
            "beta": "GHIJKLYZβ",
            "gamma": "MNOPQRSTUVΣΔθΩΓ",
        }
        category = category_map.get(overall_position.get("end_position"))
        if category:
            return {
                letter: combinations
                for letter, combinations in self.letters.items()
                # if the letter is one of the letters in the category map
                if letter in category
            }
        return {}

    def get_current_letter_type(self):
        letter = self.get_current_letter()
        if letter is not None:
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    return letter_type
        else:
            return None

    def get_start_end_locations(self):
        self.red_arrow = (
            self.arrows[0] if self.arrows[0].color == "red" else self.arrows[1]
        )
        self.blue_arrow = (
            self.arrows[0] if self.arrows[0].color == "blue" else self.arrows[1]
        )

        start_locations = (
            self.red_arrow.start_location,
            "red",
            self.blue_arrow.start_location,
            "blue",
        )
        end_locations = (
            self.red_arrow.end_location,
            "red",
            self.blue_arrow.end_location,
            "blue",
        )

        return start_locations, end_locations

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

    def create_ghost_arrow(self, arrow):
        deleted_arrow_attributes = arrow.attributes
        ghost_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow_attributes[END_LOCATION],
            END_LOCATION: deleted_arrow_attributes[END_LOCATION],
            TURNS: 0,
        }
        ghost_arrow = BlankArrow(self, ghost_attributes_dict)
        self.addItem(ghost_arrow)
        self.arrows.append(ghost_arrow)
        ghost_arrow.is_still = True
        ghost_arrow.staff = arrow.staff
        ghost_arrow.staff.arrow = ghost_arrow

    def match_combination(self, current_combination, combination):
        # Here we will compare current arrow states with the states in the combination
        current_arrows_matched = [False] * len(current_combination)
        for comb in combination:
            if "start_position" in comb and "end_position" in comb:
                # Skip the positions comparison for now
                continue
            else:
                # Compare arrow attributes
                for i, current_arrow in enumerate(current_combination):
                    if current_arrows_matched[i]:
                        continue  # this current arrow is already matched
                    if all(
                        current_arrow.get(key, None) == comb.get(key, None)
                        for key in current_arrow
                    ):
                        current_arrows_matched[i] = True
                        break  # This current_arrow matches with combination's arrow

        return all(current_arrows_matched)  # All current arrows should be matched

    ### UPDATERS ###

    def update(self):
        self.update_letter()
        self.update_arrows()
        self.update_staffs()
        self.infobox.update()

    def update_arrows(self):
        self.arrow_positioner.update_arrow_positions()

    def update_staffs(self):
        for staff in self.staffs:
            self.set_default_staff_locations(staff)

        if self.staff_positioner.staffs_in_beta():
            self.staff_positioner.reposition_beta_staffs()

    def update_letter(self):
        if len(self.staffs) == 2:
            current_letter = self.get_current_letter()
            if current_letter:
                for letter_type, letters in letter_types.items():
                    if current_letter in letters:
                        break
                svg_file = f"{LETTER_SVG_DIR}/{letter_type}/{current_letter}.svg"
                renderer = QSvgRenderer(svg_file)
                if renderer.isValid():
                    self.letter_item.setSharedRenderer(renderer)
                self.letter_item.setPos(
                    self.width() / 2 - self.letter_item.boundingRect().width() / 2,
                    self.width(),
                )

        else:
            current_letter = None
            svg_file = f"{LETTER_SVG_DIR}/blank.svg"
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                return
            self.letter_item.setSharedRenderer(renderer)
            self.letter_item.setPos(
                self.width() / 2 - self.letter_item.boundingRect().width() / 2,
                self.width(),
            )
