from PyQt6.QtCore import QPointF
from settings.numerical_constants import *
from settings.string_constants import *


class ArrowPositioner:
    def __init__(self, graphboard):
        self.letters = graphboard.letters
        self.graphboard = graphboard
        

    def update_arrow_positions(self):
        from objects.arrow.arrow import BlankArrow

        if len(self.graphboard.arrows) == 2:
            current_letter = self.graphboard.get_current_letter()
            if current_letter is not None:
                self.set_optimal_arrow_loc()
        else:
            for arrow in self.graphboard.arrows:
                if not isinstance(arrow, BlankArrow):
                    self.set_arrow_to_default_loc(arrow)

    def set_optimal_arrow_loc(self):
        current_state = self.graphboard.get_state()
        current_letter = self.graphboard.get_current_letter()

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_locations = self.find_optimal_locations(
                current_state, matching_letters
            )

            for arrow in self.graphboard.arrows:
                if not arrow.is_still:
                    if optimal_locations:
                        self.set_arrow_to_optimal_loc(optimal_locations, arrow)
                    else:
                        self.set_arrow_to_default_loc(arrow)

    def find_optimal_locations(self, current_state, matching_letters):
        for variations in matching_letters:
            if self.compare_states(current_state, variations):
                return next(
                    (
                        d
                        for d in variations
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )
        return None


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
    
    def set_arrow_to_optimal_loc(self, optimal_locations, arrow):
        optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
        pos = QPointF(
            optimal_location["x"],
            optimal_location["y"],
        )

        new_x = pos.x() - (arrow.boundingRect().width()) / 2
        new_y = pos.y() - (arrow.boundingRect().height()) / 2

        new_pos = QPointF(new_x, new_y)
        arrow.setPos(new_pos)

    def set_arrow_to_default_loc(self, arrow):
        layer2_point = arrow.graphboard.grid.get_layer2_point(arrow.quadrant)
        pos = layer2_point
        adjustment = QPointF(0, 0)

        if arrow.quadrant == NORTHEAST:
            adjustment = QPointF(DISTANCE, -DISTANCE)
        elif arrow.quadrant == SOUTHEAST:
            adjustment = QPointF(DISTANCE, DISTANCE)
        elif arrow.quadrant == SOUTHWEST:
            adjustment = QPointF(-DISTANCE, DISTANCE)
        elif arrow.quadrant == NORTHWEST:
            adjustment = QPointF(-DISTANCE, -DISTANCE)

        new_pos = QPointF(
            pos.x() + adjustment.x() + arrow.graphboard.padding,
            pos.y() + adjustment.y() + arrow.graphboard.padding,
        )

        final_pos = QPointF(new_pos.x(), new_pos.y())
        arrow.setPos(final_pos - arrow.center)
