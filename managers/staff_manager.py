from PyQt6.QtCore import QPointF, pyqtSignal, QObject
from objects.arrow import Arrow
from settings import *
from objects.staff import Staff
from managers.json_manager import Json_Manager
import math

class Staff_Manager(QObject):

    positionChanged = pyqtSignal(str)

    def __init__(self, graphboard_scene):
        super().__init__()
        self.graphboard_scene = graphboard_scene  # Scene where the staffs will be drawn
        self.beta_staves = []  # List to hold beta staves
        self.previous_position = None  # Store the previous position of staffs
        json_manager = Json_Manager(graphboard_scene)
        self.letters = json_manager.load_all_letters() 

    def connect_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker

    def create_staff(self, end_location, scene, color, context):
        
        """
        Create a staff for the specified end location, color, and context.

        Parameters:
            end_location (str): The end location of the staff ('N', 'S', 'E', 'W').
            scene (QGraphicsScene): The scene where the staff will be added.
            color (str): The color of the staff ('red', 'blue').
            context (str): The context in which the staff is being created ('main', 'mini').

        Returns:
            Staff: The newly created staff object.
        """

        # Construct the file path for the staff image based on the context
        image_file = f'images\\staves\\{end_location}_staff_{color}.svg'

        # Create a new staff object
        new_staff = Staff(
            f'{end_location}_staff',
            scene,
            self.staff_locations[f'{end_location}_staff'],
            'vertical' if end_location in ['N', 'S'] else 'horizontal',
            color,
            image_file
        )

        new_staff.staff_manager = self  # Set the staff manager reference

        # Depending on the context, you might set different properties or add additional behavior
        if context == 'pictograph':
            # Set properties specific to the mini graphboard, such as scaling or position adjustments
            new_staff.setScale(PICTOGRAPH_SCALE)  # Example of setting a different scale for the mini context
        elif context == 'graphboard':
            new_staff.setScale(GRAPHBOARD_SCALE)  # Example of setting a different scale for the main context
            # Set properties specific to the main graphboard
            # (if there are any specific properties or behaviors, they should be set here)

        # Add the staff to the scene if it's not already there
        if new_staff.scene is not scene:
            scene.addItem(new_staff)

        return new_staff


    ### MINI_GRAPHBOARD ###

    def init_pictograph_staffs(self, mini_graphboard_view, pictograph):
        # Calculate scaling and padding factors for the grid
        # Get the pictograph's transformation matrix
        self.pictograph = pictograph
        self.mini_graphboard_view = mini_graphboard_view

        # Calculate the handpoints on the graphboard based on the grid
        graphboard_handpoints = {}
        for point_name in ['N_hand_point', 'E_hand_point', 'S_hand_point', 'W_hand_point']:
            cx, cy = self.pictograph.get_circle_coordinates(point_name)
            graphboard_handpoints[point_name] = QPointF(cx, cy)


        # Initialize the staff locations based on the handpoints
        self.staff_locations = {
            'N_staff': graphboard_handpoints['N_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING),
            'E_staff': graphboard_handpoints['E_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING, - STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING),
            'S_staff': graphboard_handpoints['S_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING),
            'W_staff': graphboard_handpoints['W_hand_point'] * PICTOGRAPH_SCALE + QPointF(-STAFF_LENGTH/2 + PICTOGRAPH_GRID_PADDING, -STAFF_WIDTH/2 + PICTOGRAPH_GRID_PADDING)
        }


        # Create and hide the staffs for each direction and color
        self.staffs_on_board = {}

    def update_pictograph_staffs(self, scene):
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
                
                    new_staff = self.create_staff(end_location, scene, color, 'mini')
                    new_staff.setScale(PICTOGRAPH_SCALE)
                    arrow.staff = new_staff
                    new_staff.arrow = arrow
                    self.arrow_manager = new_staff.arrow.arrow_manager
                        
                    if new_staff.scene is not self.graphboard_scene:
                        self.graphboard_scene.addItem(new_staff)
                    self.staffs_on_board[end_location + "_staff_" + color] = new_staff  # Add the new staff to the dictionary
        self.check_and_replace_pictograph_staffs()
    
    def check_and_replace_pictograph_staffs(self):
        staff_positions = [(staff.pos().x(), staff.pos().y()) for staff in self.staffs_on_board.values() if staff.isVisible()]

        for position in set(staff_positions):
            count = staff_positions.count(position)
            if count == 2:  # Two staffs are overlapping
                beta_staffs = [staff for staff in self.staffs_on_board.values() if (staff.pos().x(), staff.pos().y()) == position]

                # Assuming the first staff's end_location can be used to determine orientation for both
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
                self.graphboard_scene.update()

    ### MAIN GRAPHBOARD ###

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
        self.staffs_on_board = {}

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
        for staff in self.staffs_on_board.values():
            if staff.scene == self.graphboard_scene: 
                self.graphboard_scene.removeItem(staff) 
        self.staffs_on_board.clear() 

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
                    
                    if staff_key in self.staffs_on_board:
                        staff = self.staffs_on_board[staff_key]
                        staff.setPos(self.staff_locations[end_location + "_staff"])  
                        staff.show()
                        
                    else:
                        new_staff = self.create_staff(end_location, graphboard_scene, color, 'main')
                        new_staff.setScale(arrow.scale())
                        arrow.staff = new_staff
                        arrow.staff.arrow = arrow
                        self.arrow_manager = new_staff.arrow.arrow_manager

                        if new_staff.scene is not self.graphboard_scene:
                            self.graphboard_scene.addItem(new_staff)
                        self.staffs_on_board[staff_key] = new_staff
                        staff = new_staff

                    updated_staffs[staff_key] = staff

        staff_keys_to_remove = set(self.staffs_on_board.keys()) - set(updated_staffs.keys())
        
        for key in staff_keys_to_remove:
            staff = self.staffs_on_board.pop(key)
            self.graphboard_scene.removeItem(staff)

        self.check_replace_beta_staffs(graphboard_scene)

        
    def hide_all_graphboard_staffs(self):
        for item in self.graphboard_scene.items():
            if isinstance(item, Staff):
                item.hide()


        self.staffs_on_board.clear() 

    def check_replace_beta_staffs(self, graphboard_scene):
        graphboard_state = self.graphboard_view.get_graphboard_state()
        if len(self.staffs_on_board) == 2:
            staffs_list = list(self.staffs_on_board.items())
            if staffs_list[0][1].arrow.end_location == staffs_list[1][1].arrow.end_location:
                self.reposition_staffs(graphboard_scene, graphboard_state)     

    def get_distance_from_center(self, position):
        """Calculate the Euclidean distance from the center point."""
        center_point = QPointF(GRAPHBOARD_WIDTH / 2, GRAPHBOARD_WIDTH / 2)  # Assuming this is the center point of your coordinate system
        # Extract the coordinates from the dictionaries
        x_position = position.get('x', 0.0)
        y_position = position.get('y', 0.0)
        center_x = center_point.x()
        center_y = center_point.y()

        # Calculate the distance
        distance = math.sqrt((x_position - center_x) ** 2 + (y_position - center_y) ** 2)
        return distance
    
    def get_optimal_staff_positions(self, arrow):
        """
        Retrieve the optimal staff positions for a given arrow based on its color and the current state.
        This method assumes that 'self.letters' and 'self.graphboard_view' are accessible within this class.
        """
        current_state = self.graphboard_view.get_graphboard_state()
        current_letter = self.info_tracker.determine_current_letter_and_type()[0]

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_staff_locations(current_state, matching_letters, arrow)

            if optimal_location:
                return optimal_location

        return None  # Return None if there are no optimal positions

    def find_optimal_staff_locations(self, current_state, matching_letters, arrow):
        """
        Find the optimal staff locations based on the current state and the matching letters.
        This is similar to 'find_optimal_locations' but specific for staff positioning.
        """
        for variations in matching_letters:
            if self.arrow_manager.compare_states(current_state, variations):
                # Search for the dictionary entry containing the optimal locations
                optimal_entry = next((d for d in variations if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)

                if optimal_entry:
                    # If the entry is found, return the optimal location for the specific arrow
                    color_key = f"optimal_{arrow['color']}_location"
                    return optimal_entry.get(color_key)

        return None 

    def reposition_beta_to_beta(self, graphboard_scene, arrows):
        """Reposition staffs when arrows have the same start location."""
        if len(arrows) != 2:
            return  # We're only handling cases where there are exactly two arrows

        arrow1, arrow2 = arrows
        same_motion = arrow1['motion_type'] == arrow2['motion_type'] in ['pro', 'anti']

        if same_motion: # Letter "G" or "H"
            # Determine which arrow is further from the center based on optimal positions
            optimal_position1 = self.get_optimal_staff_positions(arrow1)
            optimal_position2 = self.get_optimal_staff_positions(arrow2)

            distance1 = self.get_distance_from_center(optimal_position1)
            distance2 = self.get_distance_from_center(optimal_position2)

            further_arrow = arrow1 if distance1 > distance2 else arrow2
            closer_arrow = arrow2 if distance1 > distance2 else arrow1

            # Get the corresponding staffs for the arrows
            further_staff = self.staffs_on_board[further_arrow['end_location'].capitalize() + '_staff_' + further_arrow['color']]
            closer_staff = self.staffs_on_board[closer_arrow['end_location'].capitalize() + '_staff_' + closer_arrow['color']]

            # Translate the further staff in the direction of its arrow's start location by BETA_STAFF_REPOSITION_OFFSET
            direction = self.determine_translation_direction(further_arrow)
            new_position = self.calculate_new_position(further_staff.pos(), direction)
            further_staff.setPos(new_position)
            
            #Translate the closer staff in the opposite direction of the further staff
            opposite_direction = self.get_opposite_direction(direction)
            new_position = self.calculate_new_position(closer_staff.pos(), opposite_direction)
            closer_staff.setPos(new_position)
            

        else:  # hybrid scenario: one 'pro' and one 'anti' - Letter "I"
            pro_arrow = arrow1 if arrow1['motion_type'] == 'pro' else arrow2
            anti_arrow = arrow2 if arrow1['motion_type'] == 'pro' else arrow1

            pro_staff = self.staffs_on_board[pro_arrow['end_location'].capitalize() + '_staff_' + pro_arrow['color']]
            anti_staff = self.staffs_on_board[anti_arrow['end_location'].capitalize() + '_staff_' + anti_arrow['color']]

            # Translate the pro staff in the direction of its arrow's start location by BETA_STAFF_REPOSITION_OFFSET
            direction = self.determine_translation_direction(pro_arrow)
            pro_new_position = self.calculate_new_position(pro_staff.pos(), direction)
            pro_staff.setPos(pro_new_position)

            # Translate the anti staff in the opposite direction of its arrow's start location by BETA_STAFF_REPOSITION_OFFSET
            opposite_direction = self.get_opposite_direction(direction)
            anti_new_position = self.calculate_new_position(anti_staff.pos(), opposite_direction)
            anti_staff.setPos(anti_new_position)

        graphboard_scene.update()

    def determine_translation_direction(self, arrow_state):
        """Determine the translation direction based on the arrow's state."""
        if arrow_state['motion_type'] in ['pro', 'anti']:
            if arrow_state['end_location'] in ['n', 's']:
                return RIGHT if arrow_state['start_location'] == 'e' else LEFT
            elif arrow_state['end_location'] in ['e', 'w']:
                return DOWN if arrow_state['start_location'] == 's' else UP
        return None

    def calculate_new_position(self, current_position, direction):
        """Calculate the new position based on the direction."""
        offset = QPointF(BETA_STAFF_REPOSITION_OFFSET * GRAPHBOARD_SCALE, 0) if direction in [LEFT, RIGHT] else QPointF(0, BETA_STAFF_REPOSITION_OFFSET * GRAPHBOARD_SCALE)
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        else:
            return current_position - offset

    def reposition_staffs(self, graphboard_scene, graphboard_state):
        shifts = {} 


    # First, we group the arrows based on their start locations.
        arrows_grouped_by_start = {}
        for arrow in graphboard_state['arrows']:
            start_location = arrow['start_location']
            if start_location in arrows_grouped_by_start:
                arrows_grouped_by_start[start_location].append(arrow)
            else:
                arrows_grouped_by_start[start_location] = [arrow]

        # Dictionary to keep track of processed staffs to ensure they are not moved more than once.
        processed_staffs = set()

        # Iterate over the groups of arrows.
        for start_location, arrows in arrows_grouped_by_start.items():
            if len(arrows) > 1:
                # Special handling for multiple arrows from the same start location.
                self.reposition_beta_to_beta(graphboard_scene, arrows)
            else:
                # For single arrows, determine the necessary shift based on its state.
                for arrow in arrows:  # Though 'arrows' here is a list, it contains one item in this context.
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        shifts[arrow['color']] = direction  # Record the required shift.

        # Now apply the shifts. This part is outside the above loop, so it runs after all shifts are determined.
        for arrow_state in graphboard_state['arrows']:
            current_staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow_state['color']), None)
            if current_staff and current_staff not in processed_staffs:
                direction = shifts.get(arrow_state['color'])
                if direction:
                    new_position = self.calculate_new_position(current_staff.pos(), direction)
                    current_staff.setPos(new_position)
                    processed_staffs.add(current_staff)  # Mark this staff as processed.

        # After all shifts have been applied, update the scene.
        graphboard_scene.update()

    def get_opposite_direction(self, movement):
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
        for staff in self.staffs_on_board.values():
            if staff.color == color and staff.isVisible():
                return True
        return False