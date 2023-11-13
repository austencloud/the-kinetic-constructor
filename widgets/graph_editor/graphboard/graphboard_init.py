from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsView
from objects.grid import Grid
from objects.staff import RedStaff, BlueStaff
from settings.numerical_constants import *
from settings.string_constants import *
from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_staff import GhostStaff
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


class GraphboardInit:
    def __init__(self, graphboard):
        self.graphboard = graphboard

    def init_view(self):
        view = QGraphicsView()
        view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        view.setFixedSize(
            int(GRAPHBOARD_WIDTH * GRAPHBOARD_SCALE),
            int(GRAPHBOARD_HEIGHT * GRAPHBOARD_SCALE),
        )
        view.setScene(self.graphboard)
        view.scale(GRAPHBOARD_SCALE, GRAPHBOARD_SCALE)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.wheelEvent = lambda event: None
        return view

    def init_grid(self):
        grid = Grid(GRID_FILE_PATH)
        grid_width = grid.boundingRect().width()
        scene_width = self.graphboard.width()
        padding = (scene_width - grid_width) / 2
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)
        self.graphboard.addItem(grid)
        grid.init_handpoints()
        grid.init_layer2_points()
        self.graphboard.grid = grid
        self.graphboard.padding = padding
        return grid

    def init_staff_set(self):
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

        red_staff = RedStaff(self.graphboard, red_staff_dict)
        blue_staff = BlueStaff(self.graphboard, blue_staff_dict)

        red_staff.hide()
        blue_staff.hide()

        staff_set = {RED: red_staff, BLUE: blue_staff}
        return staff_set

    def init_ghost_arrows(self):
        red_ghost_arrow = GhostArrow(self.graphboard, RED)
        blue_ghost_arrow = GhostArrow(self.graphboard, BLUE)

        red_ghost_arrow.hide()
        blue_ghost_arrow.hide()

        ghost_arrows = {RED: red_ghost_arrow, BLUE: blue_ghost_arrow}
        return ghost_arrows

    def init_ghost_staffs(self):
        default_red_ghost_staff_attributes = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }
        
        default_blue_ghost_staff_attributes = {
            COLOR: BLUE,
            LOCATION: WEST,
            LAYER: 1,
        }
        
        red_ghost_staff = GhostStaff(self.graphboard, default_red_ghost_staff_attributes)
        blue_ghost_staff = GhostStaff(self.graphboard, default_blue_ghost_staff_attributes)

        red_ghost_staff.hide()
        blue_ghost_staff.hide()

        ghost_staffs = {RED: red_ghost_staff, BLUE: blue_ghost_staff}
        return ghost_staffs

    def init_letter_item(self):
        letter_item = QGraphicsSvgItem()
        self.graphboard.addItem(letter_item)
        return letter_item

    def init_quadrants(self, grid):
        grid_center = grid.get_circle_coordinates("center_point")

        grid_center_x = grid_center.x()
        grid_center_y = grid_center.y()

        ne_boundary = (
            grid_center_x,
            0,
            GRAPHBOARD_WIDTH,
            grid_center_y,
        )
        se_boundary = (
            grid_center_x,
            grid_center_y,
            GRAPHBOARD_WIDTH,
            GRAPHBOARD_HEIGHT,
        )
        sw_boundary = (
            0,
            grid_center_y,
            grid_center_x,
            GRAPHBOARD_HEIGHT,
        )
        nw_boundary = (
            0,
            0,
            grid_center_x,
            grid_center_y,
        )
        quadrants = {
            NORTHEAST: ne_boundary,
            SOUTHEAST: se_boundary,
            SOUTHWEST: sw_boundary,
            NORTHWEST: nw_boundary,
        }
        return quadrants
