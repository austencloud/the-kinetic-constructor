

    ### GRAPHBOARD ###
from managers.staff_managers.staff_manager import Staff_Manager
from PyQt6.QtCore import QPointF
from settings import GRAPHBOARD_SCALE, STAFF_LENGTH, STAFF_WIDTH
from objects.staff import Staff
from objects.arrow import Arrow
from settings import GRAPHBOARD_SCALE
class Graphboard_Staff_Manager(Staff_Manager):
    def __init__(self, main_widget, scene):
        super().__init__(main_widget)
        self.scene = scene
        self.staffs_on_board = {}
        self.staff_xy_locations = {}
        self.graphboard_view = None
    
    def init_graphboard_staffs(self, graphboard_view):
        # Calculate scaling and padding factors for the grid
        scale = self.grid.scale()

        GRID_WIDTH = self.grid.get_width()
        GRAPHBOARD_WIDTH = graphboard_view.width()
        GRAPHBOARD_HEIGHT = graphboard_view.height()
        
        self.PICTOGRAPH_GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (GRAPHBOARD_HEIGHT - GRAPHBOARD_WIDTH) / 2

        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + self.PICTOGRAPH_GRID_PADDING
            scaled_y = y * scale + self.PICTOGRAPH_GRID_PADDING
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        # Initialize the staff locations based on the handpoints
        self.staff_xy_locations = {
            'N': graphboard_handpoints['N_hand_point'] + QPointF(0, 0),
            'E': graphboard_handpoints['E_hand_point'] + QPointF(0, 0),
            'S': graphboard_handpoints['S_hand_point'] + QPointF(0, 0),
            'W': graphboard_handpoints['W_hand_point'] + QPointF(0, 0)
        }

        # Create and hide the staffs for each direction and color
        self.staffs_on_board = {}
        
    def update_graphboard_staffs(self, scene):
        for staff in scene.items():
            if isinstance(staff, Staff):
                scene.removeItem(staff)

        updated_staffs = {}
        
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                location = arrow.end_location

                if location:
                    location = location.capitalize()
                    color = ''
                    if arrow.color in ["#ed1c24", 'red']:
                        color = 'red'
                    elif arrow.color in ["#2e3192", 'blue']:
                        color = 'blue'
                    else:
                        continue

                    staff_key = location + "_staff_" + color
                    
                    new_staff = self.create_staff(location, scene, color, 'graphboard')
                    new_staff.setScale(arrow.scale())
                    arrow.staff = new_staff
                    arrow.staff.arrow = arrow
                    self.staffs_on_board[staff_key] = new_staff
                    staff = new_staff

                    updated_staffs[staff_key] = staff

        staff_keys_to_remove = set(self.staffs_on_board.keys()) - set(updated_staffs.keys())
        
        for key in staff_keys_to_remove:
            staff = self.staffs_on_board.pop(key)
            self.scene.removeItem(staff)

        self.check_replace_beta_staffs(scene)