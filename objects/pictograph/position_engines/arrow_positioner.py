from PyQt6.QtCore import QPointF
import pandas as pd
from constants.numerical_constants import DISTANCE
from constants.string_constants import *
from objects.arrow.arrow import Arrow

from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph

from utilities.TypeChecking.TypeChecking import (
    MotionAttributesDicts,
    OptimalLocationsDicts,
)


class ArrowPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.letters = pictograph.main_widget.letters
        self.pictograph = pictograph

    def update_arrow_positions(self) -> None:
        optimal_locations = None

        if len(self.pictograph.props) == 2 and len(self.pictograph.arrows) == 2:
            if self.pictograph.current_letter:
                optimal_locations = self.find_optimal_locations()

        for arrow in self.pictograph.arrows.values():
            if not arrow.is_dragging:
                if arrow.motion:
                    if arrow.motion.motion_type is not STATIC:
                        if optimal_locations:
                            self.set_arrow_to_optimal_loc(optimal_locations, arrow)
                        else:
                            self.set_arrow_to_default_loc(arrow)

        for ghost_arrow in self.pictograph.ghost_arrows.values():
            if ghost_arrow.motion:
                if ghost_arrow.motion.motion_type is not STATIC:
                    if optimal_locations:
                        self.set_arrow_to_optimal_loc(optimal_locations, ghost_arrow)
                    else:
                        self.set_arrow_to_default_loc(ghost_arrow)

    def find_optimal_locations(self) -> pd.DataFrame | None:
        current_state_df = self.pictograph.get_state()  # This is now a DataFrame
        current_letter = self.pictograph.current_letter
        candidate_states_df = pd.DataFrame(self.letters[current_letter])

        for _, candidate_state_row in candidate_states_df.iterrows():
            if self.compare_states(
                current_state_df, candidate_state_row.to_frame().transpose()
            ):
                return candidate_state_row["optimal_locations"]
        return None

    def compare_states(
        self, current_state: pd.DataFrame, candidate_state: pd.DataFrame
    ) -> bool:
        # Assume that both dataframes have the same structure
        relevant_columns = [
            "letter",
            "start_position",
            "end_position",
            "blue_motion_type",
            "blue_rotation_direction",
            "blue_turns",
            "blue_start_location",
            "blue_end_location",
            "red_motion_type",
            "red_rotation_direction",
            "red_turns",
            "red_start_location",
            "red_end_location",
        ]

        # Sort the dataframes by color to ensure correct comparison
        current_state_sorted = current_state.sort_values(by="letter").reset_index(
            drop=True
        )
        candidate_state_sorted = candidate_state.sort_values(by="letter").reset_index(
            drop=True
        )

        return current_state_sorted[relevant_columns].equals(
            candidate_state_sorted[relevant_columns]
        )

    def set_arrow_to_optimal_loc(self, arrow: "Arrow") -> None:
        arrow.set_arrow_transform_origin_to_center()
        optimal_locations_df = pd.DataFrame("OptimalLocationsDictionary.csv")
        current_letter = self.pictograph.current_letter
        if self.pictograph.prop_type in [
            STAFF,
            FAN,
            BUUGENG,
            CLUB,
            MINIHOOP,
            TRIAD,
            DOUBLESTAR,
            QUIAD,
            CHICKEN,
        ]:
            prop_size = "small"
        else:
            prop_size = "large"
            
        end_orientation = arrow.motion.end_orientation
        
        filtered_df = optimal_locations_df[
            (optimal_locations_df["letter"] == current_letter)
            & (optimal_locations_df["prop_size"] == prop_size)
            & (optimal_locations_df[f"{arrow.color}_end_orientation"] == end_orientation)
        ]
        
        pos = QPointF(
            filtered_df[f"optimal_{arrow.color}_location"]["x"],
            filtered_df[f"optimal_{arrow.color}_location"]["y"],
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
                layer2_point = layer2_points.get(arrow.location)

                if layer2_point is None:
                    print(
                        f"Warning: No layer2_point found for arrow_location {arrow.location}"
                    )

                arrow.set_arrow_transform_origin_to_center()
                adjustment = QPointF(0, 0)

                if arrow.location == NORTHEAST:
                    adjustment = QPointF(DISTANCE, -DISTANCE)
                elif arrow.location == SOUTHEAST:
                    adjustment = QPointF(DISTANCE, DISTANCE)
                elif arrow.location == SOUTHWEST:
                    adjustment = QPointF(-DISTANCE, DISTANCE)
                elif arrow.location == NORTHWEST:
                    adjustment = QPointF(-DISTANCE, -DISTANCE)

                new_pos = QPointF(
                    layer2_point.x() + adjustment.x(),
                    layer2_point.y() + adjustment.y(),
                )
                final_pos = QPointF(new_pos.x(), new_pos.y())
                arrow.setPos(final_pos - arrow.boundingRect().center())

        elif self.pictograph.grid.grid_mode == BOX:
            if arrow.motion_type in [PRO, ANTI, FLOAT]:
                layer2_point = layer2_points.get(arrow.location)

                if layer2_point is None:
                    print(
                        f"Warning: No layer2_point found for arrow_location {arrow.location}"
                    )

                arrow.set_arrow_transform_origin_to_center()
                adjustment = QPointF(0, 0)

                if arrow.location == NORTH:
                    adjustment = QPointF(DISTANCE, -DISTANCE)
                elif arrow.location == SOUTH:
                    adjustment = QPointF(DISTANCE, DISTANCE)
                elif arrow.location == EAST:
                    adjustment = QPointF(-DISTANCE, DISTANCE)
                elif arrow.location == WEST:
                    adjustment = QPointF(-DISTANCE, -DISTANCE)

                new_pos = QPointF(
                    layer2_point.x() + adjustment.x(),
                    layer2_point.y() + adjustment.y(),
                )
                final_pos = QPointF(new_pos.x(), new_pos.y())
                arrow.setPos(final_pos - arrow.boundingRect().center())
