import typing
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QTransform
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.staff.staff import Staff
from settings.numerical_constants import *
from settings.string_constants import *
from data.letter_types import letter_types
from widgets.graph_editor.graphboard.graphboard_staff_handler import (
    GraphboardStaffHandler,
)
from widgets.graph_editor.graphboard.graphboard_info_handler import (
    GraphboardInfoHandler,
)
from widgets.graph_editor.graphboard.graphboard_context_menu_handler import (
    GraphboardContextMenuHandler,
)

from utilities.export_handler import ExportHandler


class Graphboard(QGraphicsScene):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.view = QGraphicsView()
        self.view.mousePressEvent = self.mouse_press_event
        self.set_dimensions()
        self.init_grid()
        self.init_handlers()
        self.init_staffs()
        self.init_letterbox()
        
    def set_dimensions(self):
        self.setSceneRect(0, 0, DEFAULT_GRAPHBOARD_WIDTH, DEFAULT_GRAPHBOARD_HEIGHT)
        self.view.setFixedSize(int(GRAPHBOARD_WIDTH), int(GRAPHBOARD_HEIGHT))
        self.scale = GRAPHBOARD_SCALE
        
    def init_letterbox(self):
        self.letter_renderers = {}
        self.letter_item = QGraphicsSvgItem()
        self.addItem(self.letter_item)

    def init_handlers(self):
        self.staff_handler = GraphboardStaffHandler(self.main_widget, self)
        self.info_handler = GraphboardInfoHandler(self.main_widget, self)
        self.export_manager = ExportHandler(self.staff_handler, self.grid, self)
        self.context_menu_manager = GraphboardContextMenuHandler(self)
        self.arrow_manager = self.main_widget.arrow_manager
        self.drag_manager = self.main_widget.drag_manager
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_factory = self.arrow_manager.factory
        self.staff_factory = self.staff_handler.factory

    def init_grid(self):
        self.grid = Grid(GRID_PATH)
        transform = QTransform()
        graphboard_size = self.sceneRect().size()
        grid_position = QPointF(
            (
                graphboard_size.width()
                - self.grid.boundingRect().width() * GRAPHBOARD_SCALE
            )
            / 2,
            (
                graphboard_size.height()
                - self.grid.boundingRect().height() * GRAPHBOARD_SCALE
            )
            / 2
            - (VERTICAL_OFFSET),
        )

        transform.translate(grid_position.x(), grid_position.y())
        self.grid.setTransform(transform)
        self.addItem(self.grid)

    def init_staffs(self):
        self.staff_handler.init_handpoints()
        self.staff_handler.initializer.init_staffs(self)

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

    def get_quadrant_center(self, quadrant):
        graphboard_layer2_points = {}
        for point_name in [
            "NE_layer2_point",
            "SE_layer2_point",
            "SW_layer2_point",
            "NW_layer2_point",
        ]:
            cx, cy = self.grid.get_circle_coordinates(point_name)
            graphboard_layer2_points[point_name] = QPointF(cx, cy)

        centers = {
            NE: graphboard_layer2_points["NE_layer2_point"],
            SE: graphboard_layer2_points["SE_layer2_point"],
            SW: graphboard_layer2_points["SW_layer2_point"],
            NW: graphboard_layer2_points["NW_layer2_point"],
        }

        return centers.get(quadrant, QPointF(0, 0))

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
        letter = self.info_handler.determine_current_letter_and_type()[0]
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
            GRAPHBOARD_WIDTH,
        )

    def get_graphboard_quadrants(self, mouse_pos):
        scene_H_center = self.sceneRect().width() / 2
        scene_V_center = self.sceneRect().height() / 2
        adjusted_mouse_y = mouse_pos.y() + VERTICAL_OFFSET

        if adjusted_mouse_y < scene_V_center:
            if mouse_pos.x() < scene_H_center:
                quadrant = NW
            else:
                quadrant = NE
        else:
            if mouse_pos.x() < scene_H_center:
                quadrant = SW
            else:
                quadrant = SE

        return quadrant

    def mouse_press_event(self, event):
        print("mouse press event")

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.graphboard_scene.selectedItems()
        if isinstance(clicked_item, Arrow):
            self.context_menu_manager.create_arrow_menu(selected_items, event)
        elif isinstance(clicked_item, Staff):
            self.context_menu_manager.create_staff_menu(selected_items, event)
        else:
            self.context_menu_manager.create_graphboard_menu(event)