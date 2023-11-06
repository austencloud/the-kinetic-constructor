import typing
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform, QPen
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.staff.staff import Staff
from settings.numerical_constants import *
from settings.string_constants import *
from data.letter_types import letter_types
from data.start_end_location_mapping import start_end_location_mapping
from widgets.graph_editor.graphboard.graphboard_context_menu_handler import (
    GraphboardContextMenuHandler,
)

from utilities.export_handler import ExportHandler


class Graphboard(QGraphicsScene):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.setSceneRect(0, 0, 750, 900)
        self.scale = GRAPHBOARD_SCALE

        self.setup_view()
        self.init_grid()
        self.init_staffs()
        self.init_handlers()
        self.init_letterbox()

    def setup_view(self):
        self.view = QGraphicsView()
        self.view.mousePressEvent = self.mouse_press_event
        self.view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.view.setFixedSize(int(750 * GRAPHBOARD_SCALE), int(900 * GRAPHBOARD_SCALE))
        self.view.setScene(self)
        self.view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.wheelEvent = lambda event: None

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
        self.hide_all_staffs(self)

    def init_letterbox(self):
        self.letters = self.main_widget.letters
        self.letter_renderers = {}
        self.letter_item = QGraphicsSvgItem()
        self.addItem(self.letter_item)

    def init_handlers(self):
        self.export_manager = ExportHandler(self.grid, self)
        self.context_menu_manager = GraphboardContextMenuHandler(self)
        self.drag_manager = self.main_widget.drag_manager

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
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.removeItem(item)
                del item

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

    def hide_all_staffs(self, scene):
        for item in scene.items():
            if isinstance(item, Staff):
                item.setVisible(False)



    def get_graphboard_quadrants(self, mouse_pos):
        scene_H_center = self.sceneRect().width() / 2
        scene_V_center = self.sceneRect().height() / 2
        adjusted_mouse_y = mouse_pos.y() + VERTICAL_OFFSET

        if adjusted_mouse_y < scene_V_center:
            if mouse_pos.x() < scene_H_center:
                quadrant = NORTHWEST
            else:
                quadrant = NORTHEAST
        else:
            if mouse_pos.x() < scene_H_center:
                quadrant = SOUTHWEST
            else:
                quadrant = SOUTHEAST

        return quadrant

    def mouse_press_event(self, event):
        event_pos = event.pos()
        scene_pos = self.view.mapToScene(event_pos)
        pass

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.graphboard_scene.selectedItems()
        if isinstance(clicked_item, Arrow):
            self.context_menu_manager.create_arrow_menu(selected_items, event)
        elif isinstance(clicked_item, Staff):
            self.context_menu_manager.create_staff_menu(selected_items, event)
        else:
            self.context_menu_manager.create_graphboard_menu(event)

    def update_arrow_position(self, arrows):
        letter = self.determine_current_letter_and_type()[
            0
        ]
        if letter is not None:
            arrows[0].positioner.set_optimal_arrow_pos(arrows)
        else:
            for arrow in arrows:
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

    def delete_arrow(self, arrow, keep_staff=False):
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                self.removeItem(arrow)
                if keep_staff:
                    arrow.initialize_ghost_arrow(arrow, self)
                else:
                    self.removeItem(arrow.staff)

            self.update()
            
    def delete_staff(self, staff):
        self.removeItem(staff)
        self.removeItem(staff.arrow)
        self.update()
        self.update_letter(
            self.determine_current_letter_and_type()[0]
        )
        
