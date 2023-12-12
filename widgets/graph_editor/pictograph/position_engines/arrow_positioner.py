from PyQt6.QtCore import QPointF
from constants.numerical_constants import DISTANCE
from constants.string_constants import *
from objects.arrow import Arrow

from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph

from utilities.TypeChecking.TypeChecking import MotionAttributes, OptimalLocationsDicts


class ArrowPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.letters = pictograph.letters
        self.pictograph = pictograph

    def update_arrow_positions(self) -> None:
        for arrow in self.pictograph.arrows:
            arrow.setTransformOriginPoint(0, 0)
        optimal_locations = None

        if len(self.pictograph.props) == 2 and len(self.pictograph.arrows) == 2:
            if self.pictograph.current_letter:
                optimal_locations = self.find_optimal_locations()

        for arrow in self.pictograph.arrows:
            if arrow.motion.motion_type is not STATIC:
                if optimal_locations:
                    self.set_arrow_to_optimal_loc(optimal_locations, arrow)
                else:
                    self.set_arrow_to_default_loc(arrow)

    def find_optimal_locations(self) -> OptimalLocationsDicts | None:
        current_state: List[Dict[MotionAttributes, str]] = self.pictograph.get_state()
        current_letter = self.pictograph.current_letter
        current_letter_variants = self.letters[current_letter]

        variant_dict1 = {
            COLOR: current_state[0][COLOR],
            MOTION_TYPE: current_state[0][MOTION_TYPE],
            ROTATION_DIRECTION: current_state[0][ROTATION_DIRECTION],
            ARROW_LOCATION: current_state[0][ARROW_LOCATION],
            START_LOCATION: current_state[0][START_LOCATION],
            END_LOCATION: current_state[0][END_LOCATION],
            TURNS: current_state[0][TURNS],
        }
        variant_dict2 = {
            COLOR: current_state[1][COLOR],
            MOTION_TYPE: current_state[1][MOTION_TYPE],
            ROTATION_DIRECTION: current_state[1][ROTATION_DIRECTION],
            ARROW_LOCATION: current_state[1][ARROW_LOCATION],
            START_LOCATION: current_state[1][START_LOCATION],
            END_LOCATION: current_state[1][END_LOCATION],
            TURNS: current_state[1][TURNS],
        }

        modified_state = [variant_dict1, variant_dict2]

        for variants in current_letter_variants:
            if self.compare_states(modified_state, variants):
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
                {
                    COLOR,
                    MOTION_TYPE,
                    ARROW_LOCATION,
                    ROTATION_DIRECTION,
                    START_LOCATION,
                    END_LOCATION,
                    TURNS,
                }
            )
        ]

        if len(current_state) != len(filtered_candidate_state):
            return False

        for motion in current_state:
            matching_arrows = [
                candidate_arrow
                for candidate_arrow in filtered_candidate_state
                if all(
                    motion.get(key) == candidate_arrow.get(key)
                    for key in [
                        COLOR,
                        MOTION_TYPE,
                        ARROW_LOCATION,
                        ROTATION_DIRECTION,
                        START_LOCATION,
                        END_LOCATION,
                        TURNS,
                    ]
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
        layer2_points = (
            self.pictograph.grid.diamond_layer2_points
            if self.pictograph.grid.grid_mode == DIAMOND
            else self.pictograph.grid.box_layer2_points
        )

        if self.pictograph.grid.grid_mode == DIAMOND:
            if arrow.motion_type in [PRO, ANTI, FLOAT]:
                layer2_point = layer2_points.get(arrow.arrow_location)

                if layer2_point is None:
                    print(
                        f"Warning: No layer2_point found for arrow_location {arrow.arrow_location}"
                    )

                arrow.set_arrow_transform_origin_to_center()
                adjustment = QPointF(0, 0)

                if arrow.arrow_location == NORTHEAST:
                    adjustment = QPointF(DISTANCE, -DISTANCE)
                elif arrow.arrow_location == SOUTHEAST:
                    adjustment = QPointF(DISTANCE, DISTANCE)
                elif arrow.arrow_location == SOUTHWEST:
                    adjustment = QPointF(-DISTANCE, DISTANCE)
                elif arrow.arrow_location == NORTHWEST:
                    adjustment = QPointF(-DISTANCE, -DISTANCE)

                new_pos = QPointF(
                    layer2_point.x() + adjustment.x(),
                    layer2_point.y() + adjustment.y(),
                )
                final_pos = QPointF(new_pos.x(), new_pos.y())
                arrow.setPos(final_pos - arrow.boundingRect().center())

        elif self.pictograph.grid.grid_mode == BOX:
            if arrow.motion_type in [PRO, ANTI, FLOAT]:
                layer2_point = layer2_points.get(arrow.arrow_location)

                if layer2_point is None:
                    print(
                        f"Warning: No layer2_point found for arrow_location {arrow.arrow_location}"
                    )

                arrow.set_arrow_transform_origin_to_center()
                adjustment = QPointF(0, 0)

                if arrow.arrow_location == NORTH:
                    adjustment = QPointF(DISTANCE, -DISTANCE)
                elif arrow.arrow_location == SOUTH:
                    adjustment = QPointF(DISTANCE, DISTANCE)
                elif arrow.arrow_location == EAST:
                    adjustment = QPointF(-DISTANCE, DISTANCE)
                elif arrow.arrow_location == WEST:
                    adjustment = QPointF(-DISTANCE, -DISTANCE)

                new_pos = QPointF(
                    layer2_point.x() + adjustment.x(),
                    layer2_point.y() + adjustment.y(),
                )
                final_pos = QPointF(new_pos.x(), new_pos.y())
                arrow.setPos(final_pos - arrow.boundingRect().center())
