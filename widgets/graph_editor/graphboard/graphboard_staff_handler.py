from objects.staff.staff_handler import StaffHandler
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow
from constants import GRAPHBOARD_GRID_PADDING, GRAPHBOARD_SCALE, STAFF_LENGTH, STAFF_WIDTH

class GraphboardStaffHandler(StaffHandler):
    def __init__(self, main_widget, scene):
        super().__init__(main_widget)
        self.scene = scene
        self.staffs_on_board = {}
        self.staff_xy_locations = {}
        self.graphboard_view = None
    
    def init_handpoints(self, graphboard_view):
        scale = GRAPHBOARD_SCALE
        padding = GRAPHBOARD_GRID_PADDING
        GRAPHBOARD_STAFF_WIDTH = STAFF_WIDTH * GRAPHBOARD_SCALE
        GRAPHBOARD_STAFF_LENGTH = STAFF_LENGTH * GRAPHBOARD_SCALE
        
        grid_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = graphboard_view.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + padding
            scaled_y = y * scale + padding
            grid_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        self.staff_xy_locations = {
            'n': grid_handpoints['N_hand_point'] + QPointF(GRAPHBOARD_STAFF_WIDTH/2, -GRAPHBOARD_STAFF_LENGTH/2),
            'e': grid_handpoints['E_hand_point'] + QPointF(-GRAPHBOARD_STAFF_LENGTH/2, - GRAPHBOARD_STAFF_WIDTH/2),
            's': grid_handpoints['S_hand_point'] + QPointF(GRAPHBOARD_STAFF_WIDTH/2, -GRAPHBOARD_STAFF_LENGTH/2),
            'w': grid_handpoints['W_hand_point'] + QPointF(-GRAPHBOARD_STAFF_LENGTH/2, - GRAPHBOARD_STAFF_WIDTH/2)
        }

        self.staffs_on_board = {}
        
    def update_graphboard_staffs(self, scene):
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                location = arrow.end_location
                
                new_staff_dict = {
                    'color': arrow.color,
                    'location': location,
                    'layer': 1
                }
                
                
                arrow.staff.attributes.update_attributes(arrow.staff, new_staff_dict)
                arrow.staff.update_appearance()
                
        self.staff_positioner.check_replace_beta_staffs(scene)