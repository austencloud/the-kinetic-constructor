from objects.staff.staff_handler import StaffManager
from PyQt6.QtCore import QPointF
from settings.numerical_constants import (
    GRAPHBOARD_GRID_PADDING,
    GRAPHBOARD_SCALE,
    STAFF_LENGTH,
    STAFF_WIDTH,
)
from settings.string_constants import NORTH, EAST, SOUTH, WEST


class GraphboardStaffHandler(StaffManager):
    def __init__(self, main_widget, scene):
        super().__init__(main_widget)
        self.scene = scene
        self.staffs_on_board = {}
        self.staff_xy_locations = {}
        self.graphboard = None

    def init_handpoints(self):
        grid = self.scene.grid

        scale = GRAPHBOARD_SCALE
        padding = GRAPHBOARD_GRID_PADDING
        GRAPHBOARD_STAFF_WIDTH = STAFF_WIDTH * GRAPHBOARD_SCALE
        GRAPHBOARD_STAFF_LENGTH = STAFF_LENGTH * GRAPHBOARD_SCALE

        grid_handpoints = {}
        for point_name in [
            "N_hand_point",
            "E_hand_point",
            "S_hand_point",
            "W_hand_point",
        ]:
            x, y = grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + padding
            scaled_y = y * scale + padding
            grid_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        self.staff_xy_locations = {
            NORTH: grid_handpoints["N_hand_point"]
            + QPointF(GRAPHBOARD_STAFF_WIDTH / 2, -GRAPHBOARD_STAFF_LENGTH / 2),
            EAST: grid_handpoints["E_hand_point"]
            + QPointF(-GRAPHBOARD_STAFF_LENGTH / 2, -GRAPHBOARD_STAFF_WIDTH / 2),
            SOUTH: grid_handpoints["S_hand_point"]
            + QPointF(GRAPHBOARD_STAFF_WIDTH / 2, -GRAPHBOARD_STAFF_LENGTH / 2),
            WEST: grid_handpoints["W_hand_point"]
            + QPointF(-GRAPHBOARD_STAFF_LENGTH / 2, -GRAPHBOARD_STAFF_WIDTH / 2),
        }

        self.staffs_on_board = {}

    def update_graphboard_staffs(self, scene):
        for staff in scene.staffs:
            staff.update_appearance()
            staff.setPos(self.staff_xy_locations[staff.location])

        self.positioner.check_replace_beta_staffs(scene)
