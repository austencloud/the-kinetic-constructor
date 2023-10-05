from PyQt5.QtCore import QPointF, pyqtSignal, QObject, Qt
from PyQt5.QtSvg import QGraphicsSvgItem
from arrow import Arrow
from constants import STAFF_WIDTH, STAFF_LENGTH, RED, BLUE
from staff import Staff

from PyQt5.QtGui import QPen, QBrush, QColor

class Staff_Manager(QObject):

    positionChanged = pyqtSignal(str)

    def __init__(self, graphboard_scene):
        super().__init__()
        self.graphboard_scene = graphboard_scene  # Scene where the staffs will be drawn
        self.beta_staves = []  # List to hold beta staves
        self.previous_position = None  # Store the previous position of staffs

    ### INITIALIZERS ###

    def init_mini_graphboard_staffs(self, graphboard_view):
        # Calculate scaling and padding factors for the grid
        scale = self.grid.scale()

        MINI_GRID_WIDTH = self.grid.get_width()
        MINI_GRAPHBOARD_WIDTH = graphboard_view.width()
        MINI_GRAPHBOARD_HEIGHT = graphboard_view.height()
        
        print(f"MINI_GRID_WIDTH: {MINI_GRID_WIDTH}")
        print(f"MINI_GRAPHBOARD_WIDTH: {MINI_GRAPHBOARD_WIDTH}")
        print(f"MINI_GRAPHBOARD_HEIGHT: {MINI_GRAPHBOARD_HEIGHT}")
        
        self.GRID_PADDING = (MINI_GRAPHBOARD_WIDTH * scale - MINI_GRID_WIDTH * scale) / 2
        self.GRID_V_OFFSET = (MINI_GRAPHBOARD_HEIGHT * scale - MINI_GRAPHBOARD_WIDTH * scale) / 2 

        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            
            cx, cy = self.grid.get_circle_coordinates(point_name)
            print(f"Raw cx: {cx}, Raw cy: {cy}")

            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + self.GRID_PADDING
            scaled_y = y * scale + self.GRID_V_OFFSET
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)
            print(f"Scaled and Offset handpoint for {point_name}: {graphboard_handpoints[point_name]}")

            #draw a red dot at each handpoint using qpen and brush
            pen = QPen(Qt.red)
            brush = QBrush(Qt.red)
            self.graphboard_scene.addEllipse(graphboard_handpoints[point_name].x(), graphboard_handpoints[point_name].y(), 10, 10, pen, brush)


        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH)
        }

        # Create and hide the staffs for each direction and color
        self.graphboard_staffs = {}
        for end_location in ['N', 'E', 'S', 'W']:
            for color in ['red', 'blue']:
                staff_key = f"{end_location}_staff_{color}"
                self.graphboard_staffs[staff_key] = Staff(
                    f"{end_location}_staff",
                    self.graphboard_scene,
                    self.staff_locations[f"{end_location}_staff"],
                    'vertical' if end_location in ['N', 'S'] else 'horizontal',
                    color,
                    f'images\\staves\\{end_location}_staff_{color}.svg',
                )



    def init_graphboard_staffs(self, graphboard_view):
        # Calculate scaling and padding factors for the grid
        scale = self.grid.scale()

        GRID_WIDTH = self.grid.get_width()
        GRAPHBOARD_WIDTH = graphboard_view.width()
        GRAPHBOARD_HEIGHT = graphboard_view.height()
        print(f"GRID_WIDTH: {GRID_WIDTH}")
        print(f"GRAPHBOARD_WIDTH: {GRAPHBOARD_WIDTH}")
        print(f"GRAPHBOARD_HEIGHT: {GRAPHBOARD_HEIGHT}")
        
        
        self.GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (GRAPHBOARD_HEIGHT - GRAPHBOARD_WIDTH) / 2

        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale + self.GRID_PADDING
            scaled_y = y * scale + self.GRID_V_OFFSET
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH)
        }

        # Create and hide the staffs for each direction and color
        self.graphboard_staffs = {}
        for end_location in ['N', 'E', 'S', 'W']:
            for color in ['red', 'blue']:
                staff_key = f"{end_location}_staff_{color}"
                self.graphboard_staffs[staff_key] = Staff(
                    f"{end_location}_staff",
                    self.graphboard_scene,
                    self.staff_locations[f"{end_location}_staff"],
                    'vertical' if end_location in ['N', 'S'] else 'horizontal',
                    color,
                    f'images\\staves\\{end_location}_staff_{color}.svg',
                )
                self.graphboard_staffs[staff_key].hide()

    def init_propbox_staffs(self, propbox_view):
        # Define initial locations for propbox staffs
        self.propbox_staff_locations = {
            'N_staff': QPointF(100, 100),
            'E_staff': QPointF(100, 100),
            'S_staff': QPointF(100, 100),
            'W_staff': QPointF(100, 100)
        }
        
        # Create red and blue staffs in the propbox
        self.propbox_staffs = {}
        self.red_staff = Staff('red_staff', propbox_view, self.propbox_staff_locations['N_staff'], 'red', 'images\\staves\\N_staff_red.svg')
        self.blue_staff = Staff('blue_staff', propbox_view, self.propbox_staff_locations['N_staff'], 'blue', 'images\\staves\\N_staff_blue.svg')
        self.propbox_staffs['red_staff'] = self.red_staff
        self.propbox_staffs['blue_staff'] = self.blue_staff

    ### CONNECTORS ###

    def connect_grid(self, grid):
        self.grid = grid

    def connect_graphboard(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def connect_propbox(self, propbox_view):
        self.propbox_view = propbox_view

    ### UPDATERS ###

    def update_graphboard_staffs(self, scene):

        self.hide_all_graphboard_staffs()
        
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
                # print(f"update_graphboard_staffs -- arrow: {arrow}")
                end_location = arrow.end_location

                if end_location:
                    end_location = end_location.capitalize()
                    if arrow.color == "#ed1c24" or arrow.color == 'red':
                        color = 'red'
                    elif arrow.color == "#2e3192" or arrow.color == 'blue':
                        color = 'blue'
                    else:

                        continue 
                    
                    new_staff = Staff(end_location + "_staff",
                                    scene,
                                    self.staff_locations[end_location + "_staff"],
                                    'vertical' if end_location in ['N', 'S'] else 'horizontal',  # Add this line
                                    color,
                                    'images\\staves\\' + end_location + "_staff_" + color + '.svg')
                    if new_staff.scene is not self.graphboard_scene:
                        self.graphboard_scene.addItem(new_staff)
                    self.graphboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary
        self.check_and_replace_staffs()
        
        
    def hide_all_graphboard_staffs(self):
        for staff in self.graphboard_staffs.values():
            staff.hide()

    def remove_non_beta_staffs(self):
        for staff in self.graphboard_staffs.values():
            if staff.isVisible() and staff.scene is not None:
                staff.hide()  # Hide the staff

    def check_and_replace_staffs(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:  # Two staffs are overlapping
                overlapping_staffs = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]

                # Assuming the first staff's end_location can be used to determine orientation for both
                axis = overlapping_staffs[0].axis  # Replace with actual attribute if different

                if axis == 'vertical':  # Vertical staffs
                    # Move one staff 10px to the left and the other 10px to the right
                    overlapping_staffs[0].setPos(position[0] - 20, position[1])
                    overlapping_staffs[1].setPos(position[0] + 20, position[1])
                else:  # Horizontal staffs
                    # Move one staff 10px up and the other 10px down
                    overlapping_staffs[0].setPos(position[0], position[1] - 20)
                    overlapping_staffs[1].setPos(position[0], position[1] + 20)

                # Update the scene
                self.graphboard_scene.update()

    def find_staff_by_position(self, end_location):
        end_location = end_location.capitalize()
        for staff_key, staff in self.graphboard_staffs.items():
            if staff.isVisible():
                staff_end_location = staff_key.split("_")[0]
                if staff_end_location == end_location:
                    return staff  
        return None 

    def track_visible_staffs(self):
        visible_count = 0
        for staff in self.graphboard_staffs.values():
            if staff.isVisible():
                visible_count += 1
        print(f"Number of visible staves on the graphboard: {visible_count}")
