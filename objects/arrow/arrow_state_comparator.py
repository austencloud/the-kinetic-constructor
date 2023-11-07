
class ArrowStateComparator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def compare_states(self, current_state, candidate_state):
        candidate_state_dict = {
            'arrows': []
        }

        for entry in candidate_state:
            if 'color' in entry and 'motion_type' in entry:
                candidate_state_dict['arrows'].append({
                    'color': entry['color'],
                    'motion_type': entry['motion_type'],
                    'rotation_direction': entry['rotation_direction'],
                    'quadrant': entry['quadrant'],
                    'turns': entry.get('turns', 0)
                })

        if len(current_state['arrows']) != len(candidate_state_dict['arrows']):
            return False

        for arrow in current_state['arrows']:
            matching_arrows = [candidate_arrow for candidate_arrow in candidate_state_dict['arrows']
                               if all(arrow.get(key) == candidate_arrow.get(key) for key in ['color', 'motion_type', 'quadrant', 'rotation_direction'])]
            if not matching_arrows:
                return False

        return True

