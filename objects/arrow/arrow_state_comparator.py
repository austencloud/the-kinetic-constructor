from settings.string_constants import *

class ArrowStateComparator:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def compare_states(self, current_state, candidate_state):
        candidate_state_dict = {
            'arrows': []
        }
        for entry in candidate_state:
            if COLOR in entry and MOTION_TYPE in entry:
                candidate_state_dict['arrows'].append({
                    COLOR: entry[COLOR],
                    MOTION_TYPE: entry[MOTION_TYPE],
                    ROTATION_DIRECTION: entry[ROTATION_DIRECTION],
                    QUADRANT: entry[QUADRANT],
                    TURNS: entry.get(TURNS, 0)
                })

        if len(current_state['arrows']) != len(candidate_state_dict['arrows']):
            return False

        for arrow in current_state['arrows']:
            matching_arrows = [candidate_arrow for candidate_arrow in candidate_state_dict['arrows']
                               if all(arrow.get(key) == candidate_arrow.get(key) for key in [COLOR, MOTION_TYPE, QUADRANT, ROTATION_DIRECTION])]
            if not matching_arrows:
                return False

        return True

