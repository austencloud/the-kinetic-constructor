from PyQt6.QtCore import QPointF
from settings.numerical_constants import *
from settings.string_constants import *
from objects.arrow import BlankArrow, Arrow

from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard

from utilities.TypeChecking.TypeChecking import OptimalLocationsDicts


class ArrowPositioner:
    def __init__(self, graphboard: "GraphBoard") -> None:
        self.letters = graphboard.letters
        self.graphboard = graphboard

    def update(self) -> None:
        for arrow in self.graphboard.arrows:
            arrow.setTransformOriginPoint(0, 0)
        optimal_locations = None

        if len(self.graphboard.staffs) == 2:
            if self.graphboard.current_letter:
                optimal_locations = self.find_optimal_locations()

        for arrow in self.graphboard.arrows:
            if not isinstance(arrow, BlankArrow):
                if optimal_locations:
                    self.set_arrow_to_optimal_loc(optimal_locations, arrow)
                else:
                    self.set_arrow_to_default_loc(arrow)

    def find_optimal_locations(self) -> OptimalLocationsDicts | None:
        current_state = self.graphboard.get_state()
        matching_letters = self.letters[self.graphboard.current_letter]

        for variants in matching_letters:
            if self.compare_states(current_state, variants):
                return next(
                    (
                        d
                        for d in variants
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )
        return None

    def compare_states(
        self, current_state: List[Dict[str, Any]], candidate_state: List[Dict[str, Any]]
    ) -> bool:
        # Filter out non-arrow entries from candidate_state
        filtered_candidate_state = [
            entry
            for entry in candidate_state
            if set(entry.keys()).issuperset(
                {COLOR, MOTION_TYPE, QUADRANT, ROTATION_DIRECTION}
            )
        ]

        if len(current_state) != len(filtered_candidate_state):
            return False

        for arrow in current_state:
            matching_arrows = [
                candidate_arrow
                for candidate_arrow in filtered_candidate_state
                if all(
                    arrow.get(key) == candidate_arrow.get(key)
                    for key in [COLOR, MOTION_TYPE, QUADRANT, ROTATION_DIRECTION]
                )
            ]
            if not matching_arrows:
                return False

        return True

    def set_arrow_to_optimal_loc(
        self, optimal_locations: OptimalLocationsDicts, arrow: "Arrow"
    ) -> None:
        arrow.set_arrow_transform_origin_to_center()
        optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
        pos = QPointF(
            optimal_location["x"],
            optimal_location["y"],
        )

        new_x = pos.x() - (arrow.boundingRect().width()) / 2
        new_y = pos.y() - (arrow.boundingRect().height()) / 2

        new_pos = QPointF(new_x, new_y)
        arrow.setPos(new_pos)

    def set_arrow_to_default_loc(self, arrow: "Arrow") -> None:
        arrow.set_arrow_transform_origin_to_center()
        layer2_point = self.graphboard.grid.layer2_points.get(arrow.quadrant)
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
            layer2_point.x() + adjustment.x(),
            layer2_point.y() + adjustment.y(),
        )

        final_pos = QPointF(new_pos.x(), new_pos.y())
        arrow.setPos(final_pos - arrow.boundingRect().center())
