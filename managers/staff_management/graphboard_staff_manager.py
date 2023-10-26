from managers.staff_management.staff_manager import StaffManager
from PyQt6.QtCore import QPointF
from objects.staff import Staff
from objects.arrow import Arrow
from constants import GRAPHBOARD_GRID_PADDING, GRAPHBOARD_SCALE

class GraphboardStaffManager(StaffManager):
    def __init__(self, main_widget, scene):
        super().__init__(main_widget)
        self.scene = scene
        self.staffs_on_board = {}
        self.staff_xy_locations = {}
        self.graphboard_view = None
    
    def init_handpoints(self, graphboard_view):
        scale = GRAPHBOARD_SCALE
        padding = GRAPHBOARD_GRID_PADDING
        
        grid_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = graphboard_view.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + padding
            scaled_y = y * scale + padding
            grid_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        self.staff_xy_locations = {
            'n': grid_handpoints['N_hand_point'],
            'e': grid_handpoints['E_hand_point'],
            's': grid_handpoints['S_hand_point'],
            'w': grid_handpoints['W_hand_point']
        }

        self.staffs_on_board = {}
        
    def update_graphboard_staffs(self, scene):

        updated_staffs = {}
        
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                location = arrow.end_location

                if location:

                    if arrow.color in ["#ed1c24", 'red']:
                        color = 'red'
                    elif arrow.color in ["#2e3192", 'blue']:
                        color = 'blue'
                    else:
                        continue


                    new_staff_dict = {
                        'color': color,
                        'location': location,
                        'layer': 1
                    }
                    
                    new_staff = self.staff_factory.create_staff(scene, new_staff_dict)

                    staff_key = location + "_staff_" + color
                    self.staffs_on_board[staff_key] = new_staff
                    staff = new_staff

                    updated_staffs[staff_key] = staff

        staff_keys_to_remove = set(self.staffs_on_board.keys()) - set(updated_staffs.keys())
        
        for key in staff_keys_to_remove:
            staff = self.staffs_on_board.pop(key)
    

        self.staff_positioner.check_replace_beta_staffs(scene)