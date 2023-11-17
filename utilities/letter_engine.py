import json
import logging

from data.letter_engine_data import (
    motion_type_combinations,
    motion_type_letter_groups,
    parallel_combinations,
)
from data.positions_map import positions_map
from objects.arrow import Arrow
from settings.string_constants import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
from typing import TYPE_CHECKING, Dict, Literal, Set, Tuple

if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard

from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    Color,
    GammaEndingLetters,
    LetterGroupsByMotionType,
    Letters,
    MotionTypeCombinations,
    MotionTypeLetterGroupMap,
    Position,
    PreprocessedStartEndCombinations,
    RotationDirection,
    SpecificPosition,
    SpecificStartEndPositionsDicts,
    StartEndLocationTuple,
)


class LetterEngine:
    def __init__(self, graphboard: "GraphBoard") -> None:
        self.graphboard = graphboard
        self.letters = graphboard.letters
        self.preprocessed_start_end_combinations = self.preprocess_combinations()
        self.parallel_combinations: Set[
            Tuple[str, str, str, str]
        ] = parallel_combinations
        self.cached_parallel = None
        self.cached_handpath = None

    def preprocess_combinations(self) -> PreprocessedStartEndCombinations:
        preprocessed_start_end_combinations: PreprocessedStartEndCombinations = {}

        for letter, combinations in self.letters.items():
            for combination in combinations:
                start_pos: SpecificPosition = combination[0].get("start_position")
                end_pos: SpecificPosition = combination[0].get("end_position")
                if start_pos and end_pos:
                    key = f"{start_pos}_{end_pos}"
                    preprocessed_start_end_combinations.setdefault(key, []).append(
                        (letter, combination[1:])
                    )

        # Save them to a file called preprocessed.json
        with open("preprocessed.json", "w") as f:
            json.dump(preprocessed_start_end_combinations, f, indent=4)

        return preprocessed_start_end_combinations

    def get_current_letter(self) -> Letters | None:
        specific_position = self.get_specific_start_end_positions()
        if specific_position:
            start_pos = specific_position.get("start_position")
            end_pos = specific_position.get("end_position")
            preprocessed_key = f"{start_pos}_{end_pos}"
            preprocessed_group: Dict[
                Tuple[Letters, ArrowAttributesDicts]
            ] = self.preprocessed_start_end_combinations.get(preprocessed_key, [])
            preprocessed_group = {
                letter: combinations for letter, combinations in preprocessed_group
            }

            overall_position = self.get_overall_position(specific_position)
            motion_letter_group = self.get_motion_type_letter_group()

            # Convert motion_letter_group string to a set of individual letters
            motion_letter_set = set(motion_letter_group)
            filtered_letter_group = set(preprocessed_group.keys())
            # Filter the letter group based on the motion letter set
            filtered_letter_group = {
                letter
                for letter in filtered_letter_group
                if letter in motion_letter_set
            }

            if len(filtered_letter_group) != 1:
                if "gamma" in overall_position.get("end_position", "").lower():
                    filtered_letter_group = self.get_gamma_letter(filtered_letter_group)

            # Return the current letter
            if len(filtered_letter_group) == 1:
                current_letter = filtered_letter_group.pop()
                return current_letter
            else:
                logging.debug(
                    "Multiple letters returned by get_current_letter: %s",
                    filtered_letter_group,
                )
                return None
        else:
            return None

    def get_arrow(self, color: Color) -> Arrow | None:
        return next(
            (arrow for arrow in self.graphboard.arrows if arrow.color == color), None
        )

    def get_specific_start_end_positions(self) -> SpecificStartEndPositionsDicts:
        red_arrow = self.get_arrow("red")
        blue_arrow = self.get_arrow("blue")

        if red_arrow and blue_arrow:
            start_locations = (
                red_arrow.start_location,
                "red",
                blue_arrow.start_location,
                "blue",
            )
            end_locations = (
                red_arrow.end_location,
                "red",
                blue_arrow.end_location,
                "blue",
            )

            specific_position: SpecificStartEndPositionsDicts = {
                "start_position": positions_map.get(start_locations),
                "end_position": positions_map.get(end_locations),
            }

            self.red_arrow = red_arrow
            self.blue_arrow = blue_arrow
            return specific_position
        else:
            logging.warning("Red or blue arrow is missing.")
            return {}

    def get_start_end_locations_as_tuple(self) -> StartEndLocationTuple:
        self.red_arrow = (
            self.graphboard.arrows[0]
            if self.graphboard.arrows[0].color == "red"
            else self.graphboard.arrows[1]
        )
        self.blue_arrow = (
            self.graphboard.arrows[0]
            if self.graphboard.arrows[0].color == "blue"
            else self.graphboard.arrows[1]
        )

        if not self.red_arrow or not self.blue_arrow:
            logging.warning("Red or blue arrow is missing.")
            return ({}, {})

        start_locations = (
            self.red_arrow.start_location,
            "red",
            self.blue_arrow.start_location,
            "blue",
        )
        end_locations = (
            self.red_arrow.end_location,
            "red",
            self.blue_arrow.end_location,
            "blue",
        )

        return (start_locations, end_locations)

    def get_motion_type_letter_group(self) -> LetterGroupsByMotionType:
        red_motion_type = self.red_arrow.motion_type
        blue_motion_type = self.blue_arrow.motion_type

        motion_type_combination: MotionTypeCombinations = motion_type_combinations.get(
            (red_motion_type, blue_motion_type)
        )
        motion_type_letter_group: MotionTypeLetterGroupMap = (
            motion_type_letter_groups.get(motion_type_combination, "")
        )

        self.motion_type_combination = motion_type_combination
        self.motion_letter_group = motion_type_letter_group

        return motion_type_letter_group

    def is_parallel(self) -> bool:
        red_start = self.red_arrow.start_location
        red_end = self.red_arrow.end_location
        blue_start = self.blue_arrow.start_location
        blue_end = self.blue_arrow.end_location
        parallel_check_result = (
            red_start,
            red_end,
            blue_start,
            blue_end,
        ) in self.parallel_combinations

        return parallel_check_result

    def determine_handpath_direction_relationship(self) -> Literal["same", "opp", None]:
        clockwise = ["n", "e", "s", "w"]

        # Function to calculate direction
        def calculate_direction(start, end) -> RotationDirection:
            return (clockwise.index(end) - clockwise.index(start)) % len(clockwise)

        # Check if all arrow locations are valid
        arrow_locations = [
            self.red_arrow.start_location,
            self.red_arrow.end_location,
            self.blue_arrow.start_location,
            self.blue_arrow.end_location,
        ]
        if not all(location in clockwise for location in arrow_locations):
            return None

        # Calculate directions for red and blue arrows
        red_direction = calculate_direction(
            self.red_arrow.start_location, self.red_arrow.end_location
        )
        blue_direction = calculate_direction(
            self.blue_arrow.start_location, self.blue_arrow.end_location
        )

        # Determine handpath direction relationship
        handpath_direction_relationship = (
            "same" if red_direction == blue_direction else "opp"
        )
        self.handpath_direction_relationship = handpath_direction_relationship
        return handpath_direction_relationship

    def get_gamma_handpath_group(self) -> Literal["MNOPQR", "STUV"]:
        gamma_handpath_group = {
            "opp": "MNOPQR",
            "same": "STUV",
        }
        handpath_type = self.determine_handpath_direction_relationship()
        return gamma_handpath_group.get(handpath_type, "")

    def get_gamma_opp_handpath_letter_group(self) -> Literal["MNO", "PQR"]:
        if self.is_parallel():
            return "MNO"  # Return parallel group
        else:
            return "PQR"  # Return antiparallel group

    def get_gamma_letter(self, letter_group) -> GammaEndingLetters:
        gamma_handpath_letters = set(self.get_gamma_handpath_group())
        filtered_letter_group = {
            letter for letter in letter_group if letter in gamma_handpath_letters
        }

        # Opp/same handpath logic
        if any(letter in "MNOPQR" for letter in filtered_letter_group):
            gamma_opp_handpath_letters = set(self.get_gamma_opp_handpath_letter_group())
            filtered_letter_group = {
                letter
                for letter in filtered_letter_group
                if letter in gamma_opp_handpath_letters
            }

        if any(letter in "STUV" for letter in filtered_letter_group):
            if self.motion_type_combination == "pro_vs_anti":
                self.pro_arrow = (
                    self.red_arrow
                    if self.red_arrow.motion_type == "pro"
                    else self.blue_arrow
                )
                self.anti_arrow = (
                    self.red_arrow
                    if self.red_arrow.motion_type == "anti"
                    else self.blue_arrow
                )
                gamma_same_handpath_hybrid_letter = (
                    self.get_gamma_same_handpath_hybrid_letter()
                )
                filtered_letter_group = {
                    letter
                    for letter in filtered_letter_group
                    if letter == gamma_same_handpath_hybrid_letter
                }

        return filtered_letter_group

    def get_overall_position(
        self, specific_positions: SpecificStartEndPositionsDicts
    ) -> Position:
        return {position: value[:-1] for position, value in specific_positions.items()}

    def get_handpath_direction(self, start, end) -> Literal["ccw", "cw"] | None:
        """Returns COUNTER_CLOCKWISE if the handpath direction is counter-clockwise, CLOCKWISE otherwise."""
        ccw_positions = [NORTH, WEST, SOUTH, EAST]
        start_index = ccw_positions.index(start)
        end_index = ccw_positions.index(end)
        if start_index == 3 and end_index == 0:
            return COUNTER_CLOCKWISE
        elif start_index == 0 and end_index == 3:
            return CLOCKWISE
        elif start_index < end_index:
            return COUNTER_CLOCKWISE
        elif start_index > end_index:
            return CLOCKWISE

    def determine_leader_and_same_handpath_hybrid(
        self,
    ) -> Literal["leading_pro", "leading_anti"] | None:
        """Determine the leading arrow and whether the handpath is a hybrid of same-direction motion."""
        pro_handpath = self.get_handpath_direction(
            self.pro_arrow.start_location, self.pro_arrow.end_location
        )
        anti_handpath = self.get_handpath_direction(
            self.anti_arrow.start_location, self.anti_arrow.end_location
        )

        # Both arrows should have the same handpath direction, otherwise, we cannot determine a hybrid
        if pro_handpath != anti_handpath:
            logging.ERROR(
                "Cannot disambiguate U and V. Handpath directions aren't the same."
            )
            return None, ""
        else:
            handpath_direction = pro_handpath

        # Determine the leading arrow based on the counterclockwise position sequence
        ccw_positions = [NORTH, WEST, SOUTH, EAST]
        pro_start_index = ccw_positions.index(self.pro_arrow.start_location)
        anti_start_index = ccw_positions.index(self.anti_arrow.start_location)

        if (
            handpath_direction == CLOCKWISE
            and (anti_start_index - pro_start_index) % len(ccw_positions) == 1
        ):
            return "leading_pro"
        elif (
            handpath_direction == CLOCKWISE
            and (pro_start_index - anti_start_index) % len(ccw_positions) == 1
        ):
            return "leading_anti"
        elif (
            handpath_direction == COUNTER_CLOCKWISE
            and (pro_start_index - anti_start_index) % len(ccw_positions) == 1
        ):
            return "leading_pro"
        elif (
            handpath_direction == COUNTER_CLOCKWISE
            and (anti_start_index - pro_start_index) % len(ccw_positions) == 1
        ):
            return "leading_anti"

    def get_gamma_same_handpath_hybrid_letter(self) -> Literal["U", "V"]:
        gamma_same_handpath_hybrid_group = {
            "leading_pro": "U",
            "leading_anti": "V",
        }
        same_handpath_hybrid_type = self.determine_leader_and_same_handpath_hybrid()

        gamma_same_handpath_hybrid_letter: Literal[
            "U", "V"
        ] = gamma_same_handpath_hybrid_group.get(same_handpath_hybrid_type, "")
        return gamma_same_handpath_hybrid_letter
