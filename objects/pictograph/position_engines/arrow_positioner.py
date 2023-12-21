from PyQt6.QtCore import QPointF
import pandas as pd
from constants.numerical_constants import DISTANCE
from constants.string_constants import *
from objects.arrow.arrow import Arrow

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph

from utilities.TypeChecking.TypeChecking import (
    Colors,
    MotionTypes,
)


class ArrowPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.letters = pictograph.main_widget.letters
        self.pictograph = pictograph

    def update_arrow_positions(self) -> None:
        current_letter = self.pictograph.current_letter
        optimal_locations = None
        state_dict = self.pictograph.get_state()

        # Adjustments in logic to use state_dict instead of state_df
        if len(self.pictograph.props) == 2 and len(self.pictograph.arrows) == 2:
            if current_letter:
                optimal_locations = self.find_optimal_locations()

        if current_letter in ["G", "H"]:
            self.reposition_G_and_H()
        elif current_letter == "I":
            self.reposition_I()
        # elif current_letter in ["P", "Q"]:
        #     self.reposition_P_and_Q()
        # elif current_letter == "R":
        #     self.reposition_R()

        else:
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
                            self.set_arrow_to_optimal_loc(
                                optimal_locations, ghost_arrow
                            )
                        else:
                            self.set_arrow_to_default_loc(ghost_arrow)

    def find_optimal_locations(self) -> Dict | None:
        current_state = self.pictograph.get_state()
        current_letter = self.pictograph.current_letter
        candidate_states = self.letters.get(current_letter, [])

        for candidate_state in candidate_states:
            if self.compare_states(current_state, candidate_state):
                return candidate_state.get("optimal_locations")
        return None

    def compare_states(
        self, current_state: pd.DataFrame, candidate_state: pd.DataFrame
    ) -> bool:
        # Assume that both dataframes have the same structure
        relevant_keys = [
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
        return all(current_state[key] == candidate_state[key] for key in relevant_keys)

    def reposition_G_and_H(self) -> None:
        def calculate_adjustment(location, color: Colors):
            if color == RED:
                distance = 105
            elif color == BLUE:
                distance = 50
            if location == NORTHEAST:
                return QPointF(distance, -distance)
            elif location == SOUTHEAST:
                return QPointF(distance, distance)
            elif location == SOUTHWEST:
                return QPointF(-distance, distance)
            elif location == NORTHWEST:
                return QPointF(-distance, -distance)
            return QPointF(0, 0)

        red_arrow = self.pictograph.arrows.get(RED)
        blue_arrow = self.pictograph.arrows.get(BLUE)
        red_arrow.setTransformOriginPoint(red_arrow.boundingRect().center())
        blue_arrow.setTransformOriginPoint(blue_arrow.boundingRect().center())
        default_pos = self.get_default_position(red_arrow)

        red_adjustment = calculate_adjustment(red_arrow.location, RED)
        blue_adjustment = calculate_adjustment(blue_arrow.location, BLUE)
        for arrow in [red_arrow, blue_arrow]:
            if arrow.is_svg_mirrored:
                if arrow.color == BLUE:
                    if arrow.location == NORTHWEST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == SOUTHWEST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == NORTHEAST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == SOUTHEAST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                elif arrow.color == RED:
                    if arrow.location == NORTHWEST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == SOUTHWEST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == NORTHEAST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == SOUTHEAST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
            elif not arrow.is_svg_mirrored:
                if arrow.color == BLUE:
                    if arrow.location == NORTHWEST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == SOUTHWEST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == NORTHEAST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                    elif arrow.location == SOUTHEAST:
                        arrow.setPos(
                            default_pos
                            - arrow.boundingRect().center()
                            + blue_adjustment
                        )
                elif arrow.color == RED:
                    if arrow.location == NORTHWEST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == SOUTHWEST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == NORTHEAST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )
                    elif arrow.location == SOUTHEAST:
                        arrow.setPos(
                            default_pos - arrow.boundingRect().center() + red_adjustment
                        )


    def reposition_I(self) -> None:
        state = self.pictograph.get_state()

        def calculate_adjustment(location, motion_type: MotionTypes):
            if motion_type == PRO:
                distance = 100
            elif motion_type == ANTI:
                distance = 50
            if location == NORTHEAST:
                return QPointF(distance, -distance)
            elif location == SOUTHEAST:
                return QPointF(distance, distance)
            elif location == SOUTHWEST:
                return QPointF(-distance, distance)
            elif location == NORTHWEST:
                return QPointF(-distance, -distance)
            return QPointF(0, 0)

        # Determine which arrow is doing the Pro motion and which is doing the Anti motion
        pro_color, anti_color = (
            (RED, BLUE) if state["red_motion_type"] == PRO else (BLUE, RED)
        )

        # Get the arrows
        pro_arrow = self.pictograph.arrows.get(pro_color)
        anti_arrow = self.pictograph.arrows.get(anti_color)

        print(pro_arrow.transformOriginPoint())
        print(anti_arrow.transformOriginPoint())
        pro_adjustment = calculate_adjustment(pro_arrow.location, PRO)
        anti_adjustment = calculate_adjustment(anti_arrow.location, ANTI)
        # Set the default positions

        # Helper method to apply position adjustments
        def apply_adjustment(arrow, default_pos, adjustment, arrow_center):
            new_x = default_pos.x() - arrow_center.x()
            new_y = default_pos.y() - arrow_center.y()
            arrow.setPos(QPointF(new_x, new_y) + adjustment)

        for arrow in [pro_arrow, anti_arrow]:
            arrow_center = QPointF(
                arrow.boundingRect().width() / 2, arrow.boundingRect().height() / 2
            )
            default_pos = self.get_default_position(arrow)
            adjustment = (
                pro_adjustment if arrow.motion.motion_type == PRO else anti_adjustment
            )
            apply_adjustment(arrow, default_pos, adjustment, arrow_center)

            for ghost_arrow in self.pictograph.ghost_arrows.values():
                for arrow in self.pictograph.arrows.values():
                    if ghost_arrow.color == arrow.color:
                        ghost_arrow.setPos(arrow.pos())


    def set_arrow_to_default_loc(self, arrow: "Arrow") -> None:
        default_pos = self.get_default_position(arrow)
        arrow.setPos(default_pos - arrow.boundingRect().center())

    def get_default_position(self, arrow: "Arrow") -> QPointF:
        if self.pictograph.grid.grid_mode == DIAMOND:
            layer2_point = self.pictograph.grid.diamond_layer2_points.get(
                arrow.location
            )
        elif self.pictograph.grid.grid_mode == BOX:
            layer2_point = self.pictograph.grid.box_layer2_points.get(arrow.location)
        else:
            layer2_point = QPointF(0, 0)

        return layer2_point

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
            & (
                optimal_locations_df[f"{arrow.color}_end_orientation"]
                == end_orientation
            )
        ]

        pos = QPointF(
            filtered_df[f"optimal_{arrow.color}_location"]["x"],
            filtered_df[f"optimal_{arrow.color}_location"]["y"],
        )

        new_x = pos.x() - (arrow.boundingRect().width())
        new_y = pos.y() - (arrow.boundingRect().height())

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
