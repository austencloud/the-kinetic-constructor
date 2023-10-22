from PyQt6.QtCore import QPointF, pyqtSignal, QObject
from objects.arrow import Arrow
from settings import *
from objects.staff import Staff
from PyQt6.QtWidgets import QGraphicsItem
import math

class Staff_Manager(QObject):
    positionChanged = pyqtSignal(str)

    def __init__(self, main_widget):
        super().__init__()
        self.bets_staffs = []  # List to hold beta staffs
        self.previous_position = None  # Store the previous position of staffs
        self.letters = main_widget.letters
        self.grid = main_widget.grid
        self.arrow_manager = main_widget.arrow_manager
        
    def connect_info_manager(self, info_manager):
        self.info_manager = info_manager

    def create_staff(self, location, scene, color, context):
        new_staff = Staff(
            scene,
            self.staff_xy_locations[f'{location}'],
            color,
            location,
            context
        )
        return new_staff

    def connect_grid(self, grid):
        self.grid = grid
  
    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.scene = graphboard_view.scene()

        
    def hide_all_staffs(self):
        for item in self.scene.items():
            if isinstance(item, Staff):
                item.hide()

        self.staffs_on_board.clear() 

    def check_replace_beta_staffs(self, scene):
        view = scene.views()[0]
        board_state = view.get_state()
        if len(self.staffs_on_board) == 2:
            staffs_list = list(self.staffs_on_board.items())
            if staffs_list[0][1].arrow.end_location == staffs_list[1][1].arrow.end_location:
                self.reposition_staffs(scene, board_state)     

    def get_distance_from_center(self, position):
        center_point = QPointF(GRAPHBOARD_WIDTH / 2, GRAPHBOARD_WIDTH / 2)  # Assuming this is the center point of your coordinate system

        x_position = position.get('x', 0.0)
        y_position = position.get('y', 0.0)
        center_x = center_point.x()
        center_y = center_point.y()

        # Calculate the distance
        distance = math.sqrt((x_position - center_x) ** 2 + (y_position - center_y) ** 2)
        return distance
    
    def get_optimal_arrow_location(self, arrow, view):
        current_state = view.get_state()
        current_letter = view.info_manager.determine_current_letter_and_type()[0]

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location(current_state, matching_letters, arrow)

            if optimal_location:
                return optimal_location

        return None  # Return None if there are no optimal positions

    def find_optimal_arrow_location(self, current_state, matching_letters, arrow):

        for variations in matching_letters:
            if self.arrow_manager.compare_states(current_state, variations):
                # Search for the dictionary entry containing the optimal locations
                optimal_entry = next((d for d in variations if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)

                if optimal_entry:
                    # If the entry is found, return the optimal location for the specific arrow
                    color_key = f"optimal_{arrow['color']}_location"
                    return optimal_entry.get(color_key)

        return None 

    def reposition_beta_to_beta(self, scene, arrows):
        view = scene.views()[0]
        if len(arrows) != 2:
            return  # We're only handling cases where there are exactly two arrows

        arrow1, arrow2 = arrows
        same_motion = arrow1['motion_type'] == arrow2['motion_type'] in ['pro', 'anti']

        if same_motion: # Letter "G" or "H"
            # Determine which arrow is further from the center based on optimal positions
            optimal_position1 = self.get_optimal_arrow_location(arrow1, view)
            optimal_position2 = self.get_optimal_arrow_location(arrow2, view)

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

        scene.update()

    def determine_translation_direction(self, arrow_state):
        """Determine the translation direction based on the arrow's board_state."""
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

    def reposition_static_beta_staffs(self, static_arrows):
        for arrow in static_arrows:
            staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow['color']), None)
            if staff:
                if staff.location in ['N', 'S']:
                    if arrow['color'] == 'red':
                        # Move the staff to the right
                        new_position = self.calculate_new_position(staff.pos(), 'right')
                        staff.setPos(new_position)
                    elif arrow['color'] == 'blue':
                        # Move the staff to the left
                        new_position = self.calculate_new_position(staff.pos(), 'left')
                        staff.setPos(new_position)
                elif staff.location == 'E':
                    if arrow['color'] == 'red' and arrow['end_location'] == 'e':
                        # Move this staff up
                        new_position = self.calculate_new_position(staff.pos(), 'up')
                        staff.setPos(new_position)
                        # Find the other staff and move it down
                        other_staff = next((s for s in self.staffs_on_board.values() if s.location == 'E' and s != staff), None)
                        if other_staff:
                            new_position = self.calculate_new_position(other_staff.pos(), 'down')
                            other_staff.setPos(new_position)
                elif staff.location == 'W':
                    if arrow['color'] == 'blue' and arrow['end_location'] == 'w':
                        # Move this staff up
                        new_position = self.calculate_new_position(staff.pos(), 'up')
                        staff.setPos(new_position)
                        # Find the other staff and move it down
                        other_staff = next((s for s in self.staffs_on_board.values() if s.location == 'W' and s != staff), None)
                        if other_staff:
                            new_position = self.calculate_new_position(other_staff.pos(), 'down')
                            other_staff.setPos(new_position)


    def reposition_staffs(self, scene, board_state):
        translations = {} 

    # First, we group the arrows based on their start locations.
        arrows_grouped_by_start = {}
        for arrow in board_state['arrows']:
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
                # Check if all arrows have the same start and end locations
                same_start_end = all(arrow['start_location'] == arrow['end_location'] for arrow in arrows)
                
                # Special handling for multiple arrows from the same start location.
                if not same_start_end:
                    self.reposition_beta_to_beta(scene, arrows)

        # LETTERS Y AND Z - GAMMA TO BETA
        pro_or_anti_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] in ['pro', 'anti']]
        static_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] == 'static']

        if len(static_arrows) > 1:
            self.reposition_static_beta_staffs(static_arrows)
                
        if len(pro_or_anti_arrows) == 1 and len(static_arrows) == 1:
            pro_or_anti_arrow = pro_or_anti_arrows[0]
            static_arrow = static_arrows[0]

            # Calculate the direction for the "pro"/"anti" arrow's staff
            direction = self.determine_translation_direction(pro_or_anti_arrow)
            if direction:
                # Move the "pro"/"anti" arrow's staff
                pro_or_anti_staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == pro_or_anti_arrow['color']), None)
                if pro_or_anti_staff:
                    new_position = self.calculate_new_position(pro_or_anti_staff.pos(), direction)
                    pro_or_anti_staff.setPos(new_position)

                # Move the "static" arrow's staff in the opposite direction
                opposite_direction = self.get_opposite_direction(direction)
                static_staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == static_arrow['color']), None)
                if static_staff:
                    new_position = self.calculate_new_position(static_staff.pos(), opposite_direction)
                    static_staff.setPos(new_position)

        # Special handling for alpha to beta case
        converging_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] not in ['static']]
        if len(converging_arrows) == 2:
            end_locations = [arrow['end_location'] for arrow in converging_arrows]
            start_locations = [arrow['start_location'] for arrow in converging_arrows]
            
            if end_locations[0] == end_locations[1] and start_locations[0] != start_locations[1]:  # Both arrows are converging on the same location but starting from different locations
                for arrow in converging_arrows:
                    # Determine the direction for each arrow's staff
                    direction = self.determine_translation_direction(arrow)
                    
                    if direction:
                        # Move the arrow's staff
                        staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow['color']), None)
                        if staff:
                            new_position = self.calculate_new_position(staff.pos(), direction)
                            staff.setPos(new_position)

        # Now apply the translations. This part is outside the above loop, so it runs after all translations are determined.
        for arrow_state in board_state['arrows']:
            current_staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow_state['color']), None)
            if current_staff and current_staff not in processed_staffs:
                direction = translations.get(arrow_state['color'])
                if direction:
                    new_position = self.calculate_new_position(current_staff.pos(), direction)
                    current_staff.setPos(new_position)
                    processed_staffs.add(current_staff)  # Mark this staff as processed.

        # After all translations have been applied, update the scene.
        scene.update()

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
