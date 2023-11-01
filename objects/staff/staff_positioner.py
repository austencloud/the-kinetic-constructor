
from PyQt6.QtCore import QPointF
import math
from resources.constants import GRAPHBOARD_WIDTH, GRAPHBOARD_SCALE, PICTOGRAPH_SCALE, LEFT, RIGHT, UP, DOWN, BETA_OFFSET

class StaffPositioner:
    def __init__(self, staff_handler):
        self.staff_handler = staff_handler
        self.letters = staff_handler.main_widget.letters
        
    ### REPOSITIONERS ###
        
    def check_replace_beta_staffs(self, scene):
        view = scene.views()[0]
        board_state = view.get_state()
        if len(self.staff_handler.staffs_on_board) == 2:
            staffs_list = list(self.staff_handler.staffs_on_board.items())
            if staffs_list[0][1].location == staffs_list[1][1].location:
                self.reposition_staffs(scene, board_state)     
        
    def reposition_staffs(self, scene, board_state):
        view = scene.views()[0]
        scale = GRAPHBOARD_SCALE if view else PICTOGRAPH_SCALE
        processed_staffs = set()
        translations = {}

        def move_staff(staff, direction):
            new_position = self.calculate_new_position(staff.pos(), direction, scale)
            staff.setPos(new_position)

        arrows_grouped_by_start = {}
        for arrow in board_state['arrows']:
            arrows_grouped_by_start.setdefault(arrow['start_location'], []).append(arrow)

        pro_or_anti_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] in ['pro', 'anti']]
        static_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] == 'static']

        # STATIC BETA
        if len(static_arrows) > 1:
            self.reposition_static_beta(static_arrows, scale)

        # BETA → BETA - G, H, I
        for start_location, arrows in arrows_grouped_by_start.items():
            if len(arrows) > 1 and not all(arrow['start_location'] == arrow['end_location'] for arrow in arrows):
                self.reposition_beta_to_beta(scene, arrows, scale)
                

        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_arrows) == 1 and len(static_arrows) == 1:
            self.reposition_gammma_to_beta(move_staff, pro_or_anti_arrows, static_arrows)

        # ALPHA → BETA - D, E, F
        converging_arrows = [arrow for arrow in board_state['arrows'] if arrow['motion_type'] not in ['static']]
        if len(converging_arrows) == 2:
            self.reposition_alpha_to_beta(move_staff, converging_arrows)

        # Apply translations
        for arrow_state in board_state['arrows']:
            current_staff = next((staff for staff in self.staff_handler.staffs_on_board.values() if staff.arrow.color == arrow_state['color']), None)
            if current_staff and current_staff not in processed_staffs:
                direction = translations.get(arrow_state['color'])
                if direction:
                    move_staff(current_staff, direction)
                    processed_staffs.add(current_staff)

        scene.update()

    def reposition_static_beta(self, static_arrows, scale): # β
        for arrow in static_arrows:
            staff = next((staff for staff in self.staffs_on_board.values() if staff.arrow.color == arrow['color']), None)
            if not staff:
                continue

            end_location = arrow.get('end_location', '')

            beta_reposition_map = {
                ('N', 'red'): 'right',
                ('N', 'blue'): 'left',
                ('S', 'red'): 'right',
                ('S', 'blue'): 'left',
                ('E', 'red'): ('up', 'down') if end_location == 'e' else None,
                ('W', 'blue'): ('up', 'down') if end_location == 'w' else None,
            }

            action = beta_reposition_map.get((staff.location, arrow['color']), None)
            
            if action:
                if isinstance(action, str):
                    self.move_staff(staff, action, scale)
                elif isinstance(action, tuple):
                    self.move_staff(staff, action[0], scale)
                    other_staff = next((s for s in self.staff_handler.staffs_on_board.values() if s.location == staff.location and s != staff), None)
                    if other_staff:
                        self.move_staff(other_staff, action[1], scale)

    def reposition_alpha_to_beta(self, move_staff, converging_arrows): # D, E, F
        end_locations = [arrow['end_location'] for arrow in converging_arrows]
        start_locations = [arrow['start_location'] for arrow in converging_arrows]
        if end_locations[0] == end_locations[1] and start_locations[0] != start_locations[1]:
            for arrow in converging_arrows:
                direction = self.determine_translation_direction(arrow)
                if direction:
                    move_staff(next(staff for staff in self.staff_handler.staffs_on_board.values() if staff.arrow.color == arrow['color']), direction)

    def reposition_beta_to_beta(self, scene, arrows, scale): # G, H, I
        view = scene.views()[0]
        if len(arrows) != 2:
            return 

        arrow1, arrow2 = arrows
        same_motion = arrow1['motion_type'] == arrow2['motion_type'] in ['pro', 'anti']

        if same_motion:
            self.reposition_G_and_H(scale, view, arrow1, arrow2)
            
        else: 
            self.reposition_I(scale, arrow1, arrow2)

        scene.update()

    def reposition_G_and_H(self, scale, view, arrow1, arrow2):
        optimal_position1 = self.get_optimal_arrow_location(arrow1, view)
        optimal_position2 = self.get_optimal_arrow_location(arrow2, view)

        distance1 = self.get_distance_from_center(optimal_position1)
        distance2 = self.get_distance_from_center(optimal_position2)

        further_arrow = arrow1 if distance1 > distance2 else arrow2

        self.set_staff_position_based_on_arrow(further_arrow, scale)
        self.set_staff_position_based_on_arrow(arrow1 if further_arrow == arrow2 else arrow2, scale)
        
    def reposition_I(self, scale, arrow1, arrow2):
        pro_arrow = arrow1 if arrow1['motion_type'] == 'pro' else arrow2
        anti_arrow = arrow2 if arrow1['motion_type'] == 'pro' else arrow1

        self.set_staff_position_based_on_arrow(pro_arrow, scale)
        self.set_staff_position_based_on_arrow(anti_arrow, scale)

    def reposition_gammma_to_beta(self, move_staff, pro_or_anti_arrows, static_arrows): # Y, Z
        pro_or_anti_arrow, static_arrow = pro_or_anti_arrows[0], static_arrows[0]
        direction = self.determine_translation_direction(pro_or_anti_arrow)
        if direction:
            move_staff(next(staff for staff in self.staffs_on_board.values() if staff.arrow.color == pro_or_anti_arrow['color']), direction)
            move_staff(next(staff for staff in self.staffs_on_board.values() if staff.arrow.color == static_arrow['color']), self.get_opposite_direction(direction))

    ### HELPERS ### 


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
        current_letter = view.info_handler.determine_current_letter_and_type()[0]

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location(current_state, view, matching_letters, arrow)

            if optimal_location:
                return optimal_location

        return None  # Return None if there are no optimal positions

    def find_optimal_arrow_location(self, current_state, view, matching_letters, arrow_dict):
        for variations in matching_letters:
            if view.main_widget.arrow_manager.arrow_state_comparator.compare_states(current_state, variations):
                optimal_entry = next((d for d in variations if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict['color']}_location"
                    return optimal_entry.get(color_key)

        return None 

    def set_staff_position_based_on_arrow(self, arrow, scale):
        staff = self.staff_handler.staffs_on_board[arrow['end_location'] + '_staff_' + arrow['color']]
        direction = self.determine_translation_direction(arrow)
        new_position = self.calculate_new_position(staff.pos(), direction, scale)
        staff.setPos(new_position)

    def determine_translation_direction(self, arrow_state):
        """Determine the translation direction based on the arrow's board_state."""
        if arrow_state['motion_type'] in ['pro', 'anti']:
            if arrow_state['end_location'] in ['n', 's']:
                return RIGHT if arrow_state['start_location'] == 'e' else LEFT
            elif arrow_state['end_location'] in ['e', 'w']:
                return DOWN if arrow_state['start_location'] == 's' else UP
        return None

    def calculate_new_position(self, current_position, direction, scale):
        """Calculate the new position based on the direction."""
        offset = QPointF(BETA_OFFSET * scale, 0) if direction in [LEFT, RIGHT] else QPointF(0, BETA_OFFSET * scale)
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        else:
            return current_position - offset

    def get_opposite_direction(self, movement):
        if movement == 'left':
            return 'right'
        elif movement == 'right':
            return 'left'
        elif movement == 'up':
            return 'down'
        elif movement == 'down':
            return 'up'

    ### UPDATERS ###

    def update_staff_position_based_on_quadrant(self, staff, quadrant):
        new_position = self.calculate_new_position_based_on_quadrant(staff, quadrant)
        staff.setPos(new_position)
