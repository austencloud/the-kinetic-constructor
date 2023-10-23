from PyQt6.QtCore import QPointF
from constants import PICTOGRAPH_GRID_PADDING, PICTOGRAPH_SCALE
from objects.arrow import Arrow
from managers.staff_management.staff_manager import StaffManager

class PictographStaffManager(StaffManager):
    def __init__(self, main_widget, scene):
        super().__init__(main_widget)
        self.scene = scene
        self.staffs_on_board = {}
        self.staff_xy_locations = {}
        self.pictograph = None
        self.pictograph_view = None
        self.arrow_manager = None

    def connect_pictograph_view(self, pictograph_view):
        self.pictograph_view = pictograph_view
        self.scene = pictograph_view.pictograph_scene
        
    def connect_grid(self, grid):
        self.grid = grid

    def init_pictograph_staffs(self, pictograph_view, pictograph):
        self.pictograph = pictograph
        self.pictograph_view = pictograph_view
        scale = self.grid.scale()

        # Calculate the handpoints on the graphboard based on the grid
        grid_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + PICTOGRAPH_GRID_PADDING
            scaled_y = y * scale + PICTOGRAPH_GRID_PADDING
            grid_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        self.staff_xy_locations = {
            'N': grid_handpoints['N_hand_point'] ,
            'E': grid_handpoints['E_hand_point'] ,
            'S': grid_handpoints['S_hand_point'] ,
            'W': grid_handpoints['W_hand_point']  
        }

        self.staffs_on_board = {}

    def update_pictograph_staffs(self, scene):
        self.hide_all_staffs()
        
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                location = arrow.end_location

                if location:
                    location = location.capitalize()
                    if arrow.color == "#ed1c24" or arrow.color == 'red':
                        color = 'red'
                    elif arrow.color == "#2e3192" or arrow.color == 'blue':
                        color = 'blue'
                    else:

                        continue 
                
                    new_staff = self.create_staff(location, scene, color, 'pictograph')
                    new_staff.setScale(PICTOGRAPH_SCALE)
                    arrow.staff = new_staff
                    new_staff.arrow = arrow
                    self.arrow_manager = new_staff.arrow.arrow_manager
                    self.staffs_on_board[location + "_staff_" + color] = new_staff  #
                    
        self.check_replace_beta_staffs(self.scene)
    

