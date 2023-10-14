from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from objects.arrow import Arrow
from settings import *
from objects.staff import Staff


class Staff_Manager(QObject):

    positionChanged = pyqtSignal(str)

    def __init__(self, graphboard_scene):
        super().__init__()
        self.graphboard_scene = graphboard_scene  # Scene where the staffs will be drawn
        self.beta_staves = []  # List to hold beta staves
        self.previous_position = None  # Store the previous position of staffs

    ### MINI_GRAPHBOARD ###

    def init_mini_graphboard_staffs(self, mini_graphboard_view, mini_grid):
        # Calculate scaling and padding factors for the grid
        # Get the mini_grid's transformation matrix
        self.mini_grid = mini_grid
        self.mini_graphboard_view = mini_graphboard_view
        mini_grid_transform = self.mini_grid.transform()
        dx = mini_grid_transform.dx()
        dy = mini_grid_transform.dy()

        VERTICAL_BUFFER = (mini_graphboard_view.height() - mini_graphboard_view.width()) / 2

        
        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            cx, cy = self.mini_grid.get_circle_coordinates(point_name)
            graphboard_handpoints[point_name] = QPointF(cx, cy)



        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-MINI_STAFF_WIDTH, -MINI_STAFF_LENGTH - VERTICAL_BUFFER),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-MINI_STAFF_LENGTH, - MINI_STAFF_WIDTH - VERTICAL_BUFFER),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-MINI_STAFF_WIDTH, -MINI_STAFF_LENGTH - VERTICAL_BUFFER),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-MINI_STAFF_LENGTH, -MINI_STAFF_WIDTH - VERTICAL_BUFFER)
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
                # Scale down the staff
                self.graphboard_staffs[staff_key].setScale(0.5)

    def update_mini_graphboard_staffs(self, scene):
        self.hide_all_graphboard_staffs()
        
        for arrow in scene.items():
            if isinstance(arrow, Arrow):
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
                    
                                    # Scale down the new staff
                    new_staff.setScale(0.5)
                        
                    if new_staff.scene is not self.graphboard_scene:
                        self.graphboard_scene.addItem(new_staff)
                    self.graphboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary
        self.check_and_replace_mini_staffs()
    
    def check_and_replace_mini_staffs(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:  # Two staffs are overlapping
                overlapping_staffs = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]

                # Assuming the first staff's end_location can be used to determine orientation for both
                axis = overlapping_staffs[0].axis  # Replace with actual attribute if different

                if axis == 'vertical':  # Vertical staffs
                    # Move one staff 10px to the left and the other 10px to the right
                    overlapping_staffs[0].setPos(position[0] + 10, position[1])
                    overlapping_staffs[1].setPos(position[0] - 10, position[1])
                else:  # Horizontal staffs
                    # Move one staff 10px up and the other 10px down
                    overlapping_staffs[0].setPos(position[0], position[1] - 10)
                    overlapping_staffs[1].setPos(position[0], position[1] + 10)

                # Update the scene
                self.graphboard_scene.update()

    ### MAIN GRAPHBOARD ###

    def init_graphboard_staffs(self, graphboard_view):
        # Calculate scaling and padding factors for the grid
        scale = self.grid.scale()

        GRID_WIDTH = self.grid.get_width()
        GRAPHBOARD_WIDTH = graphboard_view.width()
        GRAPHBOARD_HEIGHT = graphboard_view.height()
        
        self.GRID_PADDING = (GRAPHBOARD_WIDTH - GRID_WIDTH) / 2
        self.GRID_V_OFFSET = (GRAPHBOARD_HEIGHT - GRAPHBOARD_WIDTH) / 2

        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            x, y = self.grid.get_circle_coordinates(point_name)
            scaled_x = x * scale
            scaled_y = y * scale
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2)
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

    ### PROP BOX ###

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

    def connect_mini_graphboard_view(self, mini_graphboard_view):
        self.mini_graphboard_view = mini_graphboard_view

    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def connect_propbox_view(self, propbox_view):
        self.propbox_view = propbox_view

    ### UPDATERS ###

    def update_graphboard_staffs(self, graphboard_scene):
        self.hide_all_graphboard_staffs()
        
        for arrow in graphboard_scene.items():
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
                                    graphboard_scene,
                                    self.staff_locations[end_location + "_staff"],
                                    'vertical' if end_location in ['N', 'S'] else 'horizontal',
                                    color,
                                    'images\\staves\\' + end_location + "_staff_" + color + '.svg')

                    new_staff.arrow = arrow
                    new_staff.setScale(arrow.scale())
                    arrow.staff = new_staff

                    if new_staff.scene is not self.graphboard_scene:
                        self.graphboard_scene.addItem(new_staff)
                    self.graphboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary

        self.check_replace_beta_staffs(graphboard_scene)
        
    def hide_all_graphboard_staffs(self):
        for staff in self.graphboard_staffs.values():
            staff.hide()

    def check_replace_beta_staffs(self, graphboard_scene):
        arrows = [arrow for arrow in graphboard_scene.items() if isinstance(arrow, Arrow)]
        print(f"check_replace_beta_staffs -- arrows: {arrows}")
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2: # Two staffs are overlapping
                overlapping_staffs = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]
                axis = overlapping_staffs[0].axis  
                if axis == 'vertical': 
                    overlapping_staffs[0].setPos(position[0] + 20 * GRAPHBOARD_SCALE, position[1])
                    overlapping_staffs[1].setPos(position[0] - 20 * GRAPHBOARD_SCALE, position[1])
                else: 
                    overlapping_staffs[0].setPos(position[0], position[1] - 20 * GRAPHBOARD_SCALE)
                    overlapping_staffs[1].setPos(position[0], position[1] + 20 * GRAPHBOARD_SCALE)

                self.graphboard_scene.update()

    def get_staff_position(self, staff):
        return staff.pos()

    ### GETTERS ###

    def has_staff_of_color(self, color):
        for staff in self.graphboard_staffs.values():
            if staff.color == color and staff.isVisible():
                return True
        return False