from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.staff.staff import Staff
from config.numerical_constants import *
from config.string_constants import *
from data.letter_types import letter_types
from widgets.graph_editor.graphboard.graphboard_context_menu_handler import (
    GraphboardContextMenuHandler,
)
from utilities.manipulators import Manipulators
from utilities.export_handler import ExportHandler


class Graphboard(QGraphicsScene):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.setSceneRect(0, 0, 750, 900)
        self.scale = GRAPHBOARD_SCALE
        self.init_view()
        self.init_grid()
        self.init_staffs()
        self.init_handlers()
        self.init_letterbox()
        self.init_quadrants()

    def init_view(self):
        self.view = QGraphicsView()
        self.view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.view.setFixedSize(int(750 * GRAPHBOARD_SCALE), int(900 * GRAPHBOARD_SCALE))
        self.view.setScene(self)
        self.view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.wheelEvent = lambda event: None

    def init_grid(self):
        self.grid = Grid(GRID_PATH)

        transform = QTransform()
        view_center = QPointF(self.view.width() / 2, self.view.height() / 2)

        grid_center = QPointF(
            self.grid.boundingRect().width() / 2 * GRAPHBOARD_SCALE,
            self.grid.boundingRect().height() / 2 * GRAPHBOARD_SCALE,
        )

        grid_position = QPointF(
            view_center.x() - grid_center.x(),
            view_center.y() - grid_center.y(),
        )

        transform.translate(grid_position.x(), grid_position.y())
        self.grid.setTransform(transform)

        self.grid.setPos(grid_position)
        self.addItem(self.grid)
        self.grid.init_handpoints()

    def init_staffs(self):
        staffs = []

        red_staff_dict = {
            COLOR: RED,
            LOCATION: NORTH,
            LAYER: 1,
        }
        blue_staff_dict = {
            COLOR: BLUE,
            LOCATION: SOUTH,
            LAYER: 1,
        }

        red_staff = Staff(self, red_staff_dict)
        blue_staff = Staff(self, blue_staff_dict)

        self.addItem(red_staff)
        self.addItem(blue_staff)

        staffs.append(red_staff)
        staffs.append(blue_staff)

        self.staffs = staffs
        self.hide_all_staffs()

    def init_handlers(self):
        self.manipulators = Manipulators(self)
        self.export_manager = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardContextMenuHandler(self)
        self.drag_manager = self.main_widget.drag_manager

    def init_letterbox(self):
        self.letters = self.main_widget.letters
        self.letter_renderers = {}
        self.letter_item = QGraphicsSvgItem()
        self.addItem(self.letter_item)

    def init_quadrants(self):
        grid_center = self.grid.get_circle_coordinates("center_point")
        self.grid_center_x = grid_center.x()
        self.grid_center_y = grid_center.y()

        self.ne_quadrant = (
            lambda x, y: x > self.grid_center_x and y < self.grid_center_y
        )
        self.se_quadrant = (
            lambda x, y: x > self.grid_center_x and y > self.grid_center_y
        )
        self.sw_quadrant = (
            lambda x, y: x < self.grid_center_x and y > self.grid_center_y
        )
        self.nw_quadrant = (
            lambda x, y: x < self.grid_center_x and y < self.grid_center_y
        )

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
                self.initialize_ghost_arrow(arrow, self)
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

        self.letter_item.setScale(GRAPHBOARD_SCALE)
        self.letter_item.setPos(
            self.main_widget.width() / 2
            - self.letter_item.boundingRect().width() * GRAPHBOARD_SCALE / 2,
            GRAPHBOARD_VIEW_WIDTH,
        )

    def update_staffs(self):
        for staff in self.staffs:
            staff.update_appearance()
            staff.setPos(self.grid.handpoints[staff.location])
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
        current_arrows = self.get_arrows()
        self.update_arrow_position(current_arrows)
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

    def initialize_ghost_arrow(self, arrow, graphboard):
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
        ghost_arrow.setScale(GRAPHBOARD_SCALE)
        ghost_arrow.staff = arrow.staff
        ghost_arrow.staff.arrow = ghost_arrow

    def distance(self, x1, y1, x2, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
