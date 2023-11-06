from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.staff.staff import Staff
from settings.numerical_constants import *
from settings.string_constants import *
from data.letter_types import letter_types
from events.context_menu_handler import ContextMenuHandler
from utilities.manipulators import Manipulators
from utilities.export_handler import ExportHandler
from widgets.graph_editor.graphboard.graphboard_init import GraphboardInit


class Graphboard(QGraphicsScene):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.setSceneRect(0, 0, 750, 900)
        self.initializer = GraphboardInit(self)

    def get_state(self):
        state = {
            ARROWS: [],
        }
        for item in self.items():
            if isinstance(item, Arrow):
                state[ARROWS].append(
                    {
                        COLOR: item.color,
                        MOTION_TYPE: item.motion_type,
                        ROTATION_DIRECTION: item.rotation_direction,
                        QUADRANT: item.quadrant,
                        START_LOCATION: item.start_location,
                        END_LOCATION: item.end_location,
                        TURNS: item.turns,
                    }
                )
        return state

    def get_current_arrow_positions(self):
        red_position = None
        blue_position = None

        for arrow in self.items():
            if isinstance(arrow, Arrow):
                center = arrow.pos() + arrow.boundingRect().center()
                if arrow.color == RED:
                    red_position = center
                elif arrow.color == BLUE:
                    blue_position = center
        return red_position, blue_position

    def get_arrows(self):
        current_arrows = []
        for arrow in self.items():
            if isinstance(arrow, Arrow):
                current_arrows.append(arrow)
        return current_arrows

    def get_arrows_by_color(self, color):
        return [
            item
            for item in self.items()
            if isinstance(item, Arrow) and item.color == color
        ]

    def select_all_items(self):
        for item in self.items():
            item.setSelected(True)

    def select_all_arrows(self):
        for arrow in self.items():
            if isinstance(arrow, Arrow):
                arrow.setSelected(True)

    def clear_selection(self):
        for arrow in self.selectedItems():
            arrow.setSelected(False)

    def clear_graphboard(self):
        for item in self.items():
            if isinstance(item, Arrow):
                self.removeItem(item)
            elif isinstance(item, Staff):
                item.hide()

    def delete_arrow(self, arrow, keep_staff=False):
        if isinstance(arrow, Arrow):
            self.removeItem(arrow)
            if keep_staff:
                self.create_ghost_arrow(arrow, self)
            else:
                self.delete_staff(arrow.staff)

            self.update()

    def hide_all_staffs(self):
        for item in self.staffs:
            item.hide()

    def delete_staff(self, staff):
        staff.hide()
        self.update()
        self.update_letter(self.determine_current_letter_and_type()[0])

    def update_letter(self, letter):
        letter = self.determine_current_letter_and_type()[0]
        if letter is None:
            svg_file = f"{LETTER_SVG_DIR}/blank.svg"
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                return
            self.letter_item.setSharedRenderer(renderer)

        if letter is not None:
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    break
            svg_file = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
            renderer = QSvgRenderer(svg_file)
            if not renderer.isValid():
                return
            self.letter_item.setSharedRenderer(renderer)

        self.letter_item.setPos(
            self.main_widget.width() / 2
            - self.letter_item.boundingRect().width() / 2,
            self.view.width(),
        )

    def update_staffs(self):
        for staff in self.staffs:
            staff.update_appearance()

            if staff.axis == VERTICAL:
                staff.setPos(self.grid.handpoints[staff.location] + QPointF(self.padding, self.padding) + QPointF(STAFF_WIDTH/2, -STAFF_LENGTH/2))
            else:
                staff.setPos(self.grid.handpoints[staff.location] + QPointF(self.padding, self.padding) + QPointF(-STAFF_LENGTH/2, -STAFF_WIDTH/2))
            staff.setTransformOriginPoint(0, 0)
        staff.positioner.check_replace_beta_staffs(self)

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

    def update_arrow_position(self, arrows):
        letter = self.determine_current_letter_and_type()[0]
        if letter is not None:
            arrows[0].positioner.set_optimal_arrow_pos(arrows)
        else:
            for arrow in arrows:
                if not arrow.is_still:
                    arrow.positioner.set_default_arrow_pos(arrow)

    def update(self):
        self.infobox.labels.update_type_and_position_labels()
        self.update_letter(self.determine_current_letter_and_type()[0])
        self.infobox.update()

    def determine_current_letter_and_type(self):
        current_combination = []
        arrowbox = self.main_widget.graph_editor.arrowbox

        # Check if an arrow is being dragged and add its attributes to the current_combination list
        if arrowbox.drag_preview == True:
            drag_attr = arrow.drag_preview.get_attributes()
            sorted_drag_attr = {k: drag_attr[k] for k in sorted(drag_attr.keys())}
            current_combination.append(sorted_drag_attr)

        # Add attributes of arrows already in the scene to the current_combination list
        for arrow in self.items():
            if isinstance(arrow, Arrow):
                attributes = arrow.attributes
                sorted_attributes = {
                    k: attributes[k] for k in sorted(attributes.keys())
                }
                current_combination.append(sorted_attributes)

        # Sort the list of dictionaries by the 'color' key
        current_combination = sorted(current_combination, key=lambda x: x[COLOR])

        letter_type = None
        for letter, combinations in self.letters.items():
            combinations = [
                sorted([x for x in combination if COLOR in x], key=lambda x: x[COLOR])
                for combination in combinations
            ]
            if current_combination in combinations:
                self.letter = letter
                for (
                    type,
                    letters,
                ) in letter_types.items():  # Determine the type if a letter is found
                    if self.letter in letters:
                        current_type = type
                        break
                return self.letter, current_type  # Return both values here

        self.letter = None  # Set to None if no match is found
        return self.letter, letter_type  # Always return two values

    def create_ghost_arrow(self, arrow, graphboard):
        deleted_arrow_attributes = arrow.get_attributes()
        ghost_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow_attributes[END_LOCATION],
            END_LOCATION: deleted_arrow_attributes[END_LOCATION],
            TURNS: 0,
        }

        ghost_arrow = Arrow(graphboard, ghost_attributes_dict)
        graphboard.addItem(ghost_arrow)
        ghost_arrow.is_still = True
        ghost_arrow.staff = arrow.staff
        ghost_arrow.staff.arrow = ghost_arrow

    def distance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    @staticmethod
    def point_in_boundary(x, y, boundary):
        return boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]

    def determine_quadrant(self, x, y):
        if self.point_in_boundary(x, y, self.ne_boundary):
            return NORTHEAST
        elif self.point_in_boundary(x, y, self.se_boundary):
            return SOUTHEAST
        elif self.point_in_boundary(x, y, self.sw_boundary):
            return SOUTHWEST
        elif self.point_in_boundary(x, y, self.nw_boundary):
            return NORTHWEST
        else:
            return None
