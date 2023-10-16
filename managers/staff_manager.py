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
            'N_staff': graphboard_handpoints['N_hand_point'] * PICTOGRAPH_SCALE + QPointF(-MINI_STAFF_WIDTH, -MINI_STAFF_LENGTH - VERTICAL_BUFFER),
            'E_staff': graphboard_handpoints['E_hand_point'] * PICTOGRAPH_SCALE + QPointF(-MINI_STAFF_LENGTH, - MINI_STAFF_WIDTH - VERTICAL_BUFFER),
            'S_staff': graphboard_handpoints['S_hand_point'] * PICTOGRAPH_SCALE + QPointF(-MINI_STAFF_WIDTH, -MINI_STAFF_LENGTH - VERTICAL_BUFFER),
            'W_staff': graphboard_handpoints['W_hand_point'] * PICTOGRAPH_SCALE + QPointF(-MINI_STAFF_LENGTH, -MINI_STAFF_WIDTH - VERTICAL_BUFFER)
        }


        # Create and hide the staffs for each direction and color
        self.graphboard_staffs = {}

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
                    new_staff.setScale(PICTOGRAPH_SCALE)
                        
                    if new_staff.scene is not self.graphboard_scene:
                        self.graphboard_scene.addItem(new_staff)
                    self.graphboard_staffs[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary
        self.check_and_replace_mini_staffs()
    
    def check_and_replace_mini_staffs(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.graphboard_staffs.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:  # Two staffs are overlapping
                beta_staffs = [staff for staff in self.graphboard_staffs.values() if (staff.pos().x(), staff.pos().y()) == position]

                # Assuming the first staff's end_location can be used to determine orientation for both
                axis = beta_staffs[0].axis  # Replace with actual attribute if different

                if axis == 'vertical':  # Vertical staffs
                    # Move one staff 10px to the left and the other 10px to the right
                    beta_staffs[0].setPos(position[0] + 20*PICTOGRAPH_SCALE, position[1])
                    beta_staffs[1].setPos(position[0] - 20*PICTOGRAPH_SCALE, position[1])
                else:  # Horizontal staffs
                    # Move one staff 10px up and the other 10px down
                    beta_staffs[0].setPos(position[0], position[1] - 20*PICTOGRAPH_SCALE)
                    beta_staffs[1].setPos(position[0], position[1] + 20*PICTOGRAPH_SCALE)

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
            scaled_x = x * scale + self.GRID_PADDING
            scaled_y = y * scale + self.GRID_V_OFFSET
            graphboard_handpoints[point_name] = QPointF(scaled_x, scaled_y)

        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH*GRAPHBOARD_SCALE),
            'E_staff': graphboard_handpoints['E_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH*GRAPHBOARD_SCALE),
            'S_staff': graphboard_handpoints['S_hand_point'] + QPointF(-STAFF_WIDTH / 2, -STAFF_LENGTH / 2 - STAFF_WIDTH*GRAPHBOARD_SCALE),
            'W_staff': graphboard_handpoints['W_hand_point'] + QPointF(-STAFF_LENGTH / 2, -STAFF_WIDTH / 2 - STAFF_WIDTH*GRAPHBOARD_SCALE)
        }

        # Create and hide the staffs for each direction and color
        self.graphboard_staffs = {}

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
        # First, let's properly remove all existing staffs from both the scene and the dictionary
        for staff in self.graphboard_staffs.values():
            if staff.scene == self.graphboard_scene:  # Ensure the staff is in the scene
                self.graphboard_scene.removeItem(staff)  # Remove it from the scene
                # Here, you may want to implement any other cleanup for the staff object

        self.graphboard_staffs.clear()  # Clear the dictionary after cleaning up the staff objects

            
        # A dictionary to track staffs that have been updated in this cycle
        updated_staffs = {}
        
        for arrow in graphboard_scene.items():
            if isinstance(arrow, Arrow):
                end_location = arrow.end_location

                if end_location:
                    end_location = end_location.capitalize()
                    color = ''
                    if arrow.color in ["#ed1c24", 'red']:
                        color = 'red'
                    elif arrow.color in ["#2e3192", 'blue']:
                        color = 'blue'
                    else:
                        continue

                    staff_key = end_location + "_staff_" + color
                    if staff_key in self.graphboard_staffs:
                        # Staff already exists, just update its position and make it visible
                        staff = self.graphboard_staffs[staff_key]
                        staff.setPos(self.staff_locations[end_location + "_staff"])  # update position
                        staff.show()
                    else:
                        # Create new staff
                        new_staff = Staff(end_location + "_staff",
                                        graphboard_scene,
                                        self.staff_locations[end_location + "_staff"],
                                        'vertical' if end_location in ['N', 'S'] else 'horizontal',
                                        color,
                                        'images\\staves\\' + end_location + "_staff_" + color + '.svg')

                        new_staff.setScale(arrow.scale())  # assuming you need to set scale
                        arrow.staff = new_staff
                        arrow.staff.arrow = arrow

                        if new_staff.scene is not self.graphboard_scene:
                            self.graphboard_scene.addItem(new_staff)
                        self.graphboard_staffs[staff_key] = new_staff
                        staff = new_staff

                    updated_staffs[staff_key] = staff  # Store the staff that has been updated

        # Remove any staffs that weren't updated in this cycle (no longer needed)
        staff_keys_to_remove = set(self.graphboard_staffs.keys()) - set(updated_staffs.keys())
        for key in staff_keys_to_remove:
            staff = self.graphboard_staffs.pop(key)
            # Remove the staff from the scene if you're sure you don't need it anymore
            self.graphboard_scene.removeItem(staff)

        self.check_replace_beta_staffs(graphboard_scene)

        
    def hide_all_graphboard_staffs(self):
        print(self.graphboard_scene.items())
        # Checking and hiding all staff items in the scene.
        for item in self.graphboard_scene.items():  # Iterating directly over all scene items.
            if isinstance(item, Staff):  # Checking if the current item is a Staff instance.
                item.hide()  # Hiding the staff item.
                # No need to delete staff here, as you might lose references you need. Just hide them.

        # Clear the dictionary after all staffs are processed.
        self.graphboard_staffs.clear() 

    def check_replace_beta_staffs(self, graphboard_scene):
        # First, we retrieve the current state of the graphboard.
        graphboard_state = self.graphboard_view.get_graphboard_state()

        # if there are two staves in the scene, we need to check if they have the same location, determined by the end position of their arrow.
        if len(self.graphboard_staffs) == 2:
            # Convert the dict_items to a list so they are subscriptable
            staffs_list = list(self.graphboard_staffs.items())

            # Now you can access the items by index
            if staffs_list[0][1].arrow.end_location == staffs_list[1][1].arrow.end_location:
                # If the two staves have the same location, we need to reposition them.
                self.reposition_staffs(graphboard_scene, graphboard_state)


        # We need to identify the arrows and their corresponding staffs that need repositioning.


    def reposition_staffs(self, graphboard_scene, graphboard_state):
        
    
        shifts = {} 
        
        for arrow_state in graphboard_state['arrows']:
            # Determine the direction of the shift based on the arrow's properties.
            shift_direction = None
            if arrow_state['motion_type'] in ['pro', 'anti']:
                if arrow_state['end_location'] in ['n', 's']:
                    shift_direction = 'right' if arrow_state['start_location'] == 'e' else 'left'
                elif arrow_state['end_location'] in ['e', 'w']:
                    shift_direction = 'down' if arrow_state['start_location'] == 's' else 'up'

            # Record the shift if one was determined.
            if shift_direction:
                shifts[arrow_state['color']] = shift_direction
            
        for arrow_state in graphboard_state['arrows']:
            # For each staff, we check if its corresponding arrow is the one we're analyzing.
            for staff in self.graphboard_staffs.values():
                if staff.arrow.color == arrow_state['color']:
                    current_staff = staff
                    break  # We found the corresponding staff, so we can stop this loop.
            
            if arrow_state['motion_type'] == 'pro' or arrow_state['motion_type'] == 'anti':
                if arrow_state['end_location'] == 'n' or arrow_state['end_location'] == 's':
                    if arrow_state['start_location'] == 'e':
                        new_position = current_staff.pos() + QPointF(20 * GRAPHBOARD_SCALE, 0)
                    elif arrow_state['start_location'] == 'w':
                        new_position = current_staff.pos() - QPointF(20 * GRAPHBOARD_SCALE, 0)
                elif arrow_state['end_location'] == 'e' or arrow_state['end_location'] == 'w':
                    if arrow_state['start_location'] == 'n':
                        new_position = current_staff.pos() - QPointF(0, 20 * GRAPHBOARD_SCALE)
                    elif arrow_state['start_location'] == 's':
                        new_position = current_staff.pos() + QPointF(0, 20 * GRAPHBOARD_SCALE)
            
                if new_position:
                    current_staff.setPos(new_position)
                        

            # Handling static arrows.
            if arrow_state['motion_type'] == 'static' and arrow_state['end_location'] in ['n', 's', 'e', 'w']:
                other_staff_translation_direction = None

                for other_arrow_state in graphboard_state['arrows']:
                    if other_arrow_state['motion_type'] in ['pro', 'anti'] and other_arrow_state['end_location'] == arrow_state['end_location']:
                        other_staff_translation_direction = shifts.get(other_arrow_state['color'])

                if other_staff_translation_direction:
                    opposite_movement = self.get_opposite_movement(other_staff_translation_direction)


                        # Based on the opposite movement, we adjust the position of the static staff.
                    if opposite_movement == 'left':
                        new_position = current_staff.pos() - QPointF(20 * GRAPHBOARD_SCALE, 0)
                    elif opposite_movement == 'right':
                        new_position = current_staff.pos() + QPointF(20 * GRAPHBOARD_SCALE, 0)
                    elif opposite_movement == 'up':
                        new_position = current_staff.pos() - QPointF(0, 20 * GRAPHBOARD_SCALE)
                    elif opposite_movement == 'down':
                        new_position = current_staff.pos() + QPointF(0, 20 * GRAPHBOARD_SCALE)

                    if new_position:
                        current_staff.setPos(new_position)
                    
        # After going through all arrows and making the necessary adjustments, we update the scene.
        graphboard_scene.update()

    def get_opposite_movement(self, movement):
        # This method returns the opposite movement. For example, if a dynamic staff moves left, the static one should move right.
        if movement == 'left':
            return 'right'
        elif movement == 'right':
            return 'left'
        elif movement == 'up':
            return 'down'
        elif movement == 'down':
            return 'up'

    def get_staff_position(self, staff):
        return staff.pos()

    ### GETTERS ###

    def has_staff_of_color(self, color):
        for staff in self.graphboard_staffs.values():
            if staff.color == color and staff.isVisible():
                return True
        return False