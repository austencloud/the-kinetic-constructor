from PyQt6.QtCore import QPointF
from settings import PICTOGRAPH_GRID_PADDING, PICTOGRAPH_SCALE, STAFF_LENGTH, STAFF_WIDTH, BETA_STAFF_REPOSITION_OFFSET
from objects.arrow import Arrow
from managers.staff_managers.staff_manager import Staff_Manager

class Pictograph_Staff_Manager(Staff_Manager):
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

        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            cx, cy = self.grid.get_circle_coordinates(point_name)
            graphboard_handpoints[point_name] = QPointF(cx, cy)

        self.staff_xy_locations = {
            'N': graphboard_handpoints['N_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING),
            'E': graphboard_handpoints['E_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING, - STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING),
            'S': graphboard_handpoints['S_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING),
            'W': graphboard_handpoints['W_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING)
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
                
                    new_staff = self.create_staff(location, scene, color, 'mini')
                    new_staff.setScale(PICTOGRAPH_SCALE)
                    arrow.staff = new_staff
                    new_staff.arrow = arrow
                    self.arrow_manager = new_staff.arrow.arrow_manager
                        
                    if new_staff.scene is not self.scene:
                        self.scene.addItem(new_staff)
                    self.staffs_on_board[location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary
        self.check_and_replace_pictograph_staffs()
    
    def check_and_replace_pictograph_staffs(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.staffs_on_board.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:  # Two staffs are overlapping
                beta_staffs = [staff for staff in self.staffs_on_board.values() if (staff.pos().x(), staff.pos().y()) == position]

                # Assuming the first staff's location can be used to determine orientation for both
                axis = beta_staffs[0].axis  # Replace with actual attribute if different

                if axis == 'vertical':  # Vertical staffs
                    # Move one staff 10px to the left and the other 10px to the right
                    beta_staffs[0].setPos(position[0] + BETA_STAFF_REPOSITION_OFFSET*PICTOGRAPH_SCALE, position[1])
                    beta_staffs[1].setPos(position[0] - BETA_STAFF_REPOSITION_OFFSET*PICTOGRAPH_SCALE, position[1])
                else:  # Horizontal staffs
                    # Move one staff 10px up and the other 10px down
                    beta_staffs[0].setPos(position[0], position[1] - BETA_STAFF_REPOSITION_OFFSET*PICTOGRAPH_SCALE)
                    beta_staffs[1].setPos(position[0], position[1] + BETA_STAFF_REPOSITION_OFFSET*PICTOGRAPH_SCALE)

                # Update the scene
                self.scene.update()

