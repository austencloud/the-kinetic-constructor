from email.charset import QP
import json
from PyQt6.QtCore import QPointF
from Enums import LetterNumberType
from constants import *
from objects.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Literal, Tuple, Union
from objects.motion.motion import Motion
from PyQt6.QtCore import QTimer
from utilities.TypeChecking.Letters import (
    Letters,
    Type1_hybrid_letters,
    Type1_non_hybrid_letters,
)
from utilities.TypeChecking.TypeChecking import Locations, MotionTypes


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.Type1_arrow_positioner import (
        Type1ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type2_arrow_positioner import (
        Type2ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type3_arrow_positioner import (
        Type3ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type4_arrow_positioner import (
        Type4ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type5_arrow_positioner import (
        Type5ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type6_arrow_positioner import (
        Type6ArrowPositioner,
    )


class ArrowPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.arrows = pictograph.arrows.values()
        self.readjust_timer = QTimer()
        self.readjust_timer.timeout.connect(self.update_arrow_positions)
        self.readjust_timer.start(2000)
        self.letters_to_reposition = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "X",
            "Y",
            "Z",
            "Σ",
            "Δ",
            "θ",
            "Ω",
            "Φ",
            "Ψ",
            "Λ",
            "W-",
            "X-",
            "Y-",
            "Z-",
            "Σ-",
            "Δ-",
            "θ-",
            "Ω-",
            "Λ-",
        ]
        self.generic_placement_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "S",
            "T",
            "U",
            "V",
        ]
        self.update_arrow_positions()
        
    def _load_placements(self) -> Dict[str, Dict[str, Tuple[int, int]]]:
        json_path = "arrow_placement/arrow_placements.json"
        with open(json_path, "r") as file:
            return json.load(file)

    def _convert_key_to_tuple(self, key: str) -> Tuple[int, int]:
        key_values = key.strip("()").split(", ")
        converted_values = []
        for value in key_values:
            if value.isdigit() and int(value) in [0, 1, 2, 3]:
                converted_values.append(int(value))
            else:
                converted_values.append(float(value))
        return tuple(converted_values)

    # Additional method to handle letter-specific repositioning
    def reposition_for_letter(self, letter: str) -> None:
        reposition_method = getattr(self, f"_reposition_{letter}", None)
        if reposition_method:
            reposition_method()

    ### PUBLIC METHODS ###
    def update_arrow_positions(self) -> None:
        self.letter = self.pictograph.letter
        self.placements = self._load_placements()
        for arrow in self.arrows:
            if arrow.loc and self.letter in self.letters_to_reposition:
                initial_pos = self._get_initial_position(arrow)
                adjustment = self._get_adjustment(arrow)
                new_pos = initial_pos + adjustment - arrow.boundingRect().center()
                arrow.setPos(new_pos)

    def _get_initial_position(self, arrow: Arrow) -> QPointF:
        # Set the initial position to the handpoint corresponding to the arrow's location
        layer2_points = self.pictograph.grid.get_layer2_points()
        return layer2_points.get(arrow.loc, QPointF(0, 0))

    def _get_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_values = self._get_adjustment_values(arrow)
        x, y = adjustment_values

        # Use a single method to handle both PRO and ANTI directional adjustments
        directional_adjustments = self._generate_directional_tuples(
            x, y, arrow.motion, arrow.motion_type
        )

        quadrant_index = self._get_quadrant_index(arrow.loc)
        return directional_adjustments[quadrant_index]

    def _generate_directional_tuples(
        self, x, y, motion: Motion, motion_type: str
    ) -> List[QPointF]:
        if motion_type in [PRO, STATIC]:
            if motion.prop_rot_dir in [CLOCKWISE, NO_ROT]:
                return [QPointF(x, y), QPointF(-y, x), QPointF(-x, -y), QPointF(y, -x)]
            elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [QPointF(-y, -x), QPointF(x, -y), QPointF(y, x), QPointF(-x, y)]
        elif motion_type in [ANTI, DASH]:
            if motion.prop_rot_dir in [CLOCKWISE, NO_ROT]:
                return [QPointF(-y, -x), QPointF(x, -y), QPointF(y, x), QPointF(-x, y)]
            elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [QPointF(x, y), QPointF(-y, x), QPointF(-x, -y), QPointF(y, -x)]

    def _calculate_generic_adjustment(self, arrow: Arrow, adjustment_key: str) -> Tuple[int, int]:
        with open("arrow_placement/generic_placements.json", "r") as file:
            generic_placements:Dict = json.load(file)
        # Load generic placement data
        if self.letter == 'E' and adjustment_key in ['(0.5, 0.5)', '(2.5, 2.5)', '(0.5, 2.5)', '(2.5, 0.5)']:
            adjustment_values = generic_placements.get(self.letter, {}).get(adjustment_key, {})
            return adjustment_values

        adjustment_values = generic_placements.get(arrow.motion_type, {}).get(str(arrow.turns), (0, 0))
        return adjustment_values

    def _get_adjustment_values(self, arrow: Arrow) -> Tuple[int, int]:
        blue_arrow = self.pictograph.arrows.get(BLUE)
        red_arrow = self.pictograph.arrows.get(RED)
        adjustment_key = f"({blue_arrow.turns}, {red_arrow.turns})"
        if blue_arrow.turns in [0.0, 1.0, 2.0, 3.0]:
            blue_arrow.turns = int(blue_arrow.turns)
        if red_arrow.turns in [0.0, 1.0, 2.0, 3.0]:
            red_arrow.turns = int(red_arrow.turns)

        if self.letter not in self.generic_placement_letters:
            letter_adjustments = self.placements.get(self.letter, {})
            adjustment_values: Dict = letter_adjustments.get(adjustment_key, {})
            if self.letter in Type1_hybrid_letters:
                return tuple(adjustment_values.get(arrow.motion_type, (0, 0)))
            elif self.letter in Type1_non_hybrid_letters:
                return tuple(adjustment_values.get(arrow.color, (0, 0)))
            else:
                return (0, 0)
        if self.letter in self.generic_placement_letters:
            return self._calculate_generic_adjustment(arrow, adjustment_key)
            
    def _get_quadrant_index(self, location: Locations) -> Literal[0, 1, 2, 3]:
        """Map location to index for quadrant adjustments"""
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)

    def _get_pro_anti_arrows(self, scene: "Pictograph") -> Tuple[Arrow, Arrow]:
        arrows = scene.arrows
        pro_arrow = arrows[RED] if arrows[RED].motion_type == PRO else arrows[BLUE]
        anti_arrow = arrows[RED] if arrows[RED].motion_type == ANTI else arrows[BLUE]
        return pro_arrow, anti_arrow

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_map.get(location, "")

    def are_adjacent_locations(self, location1: str, location2: str) -> bool:
        adjacent_map = {
            NORTHEAST: [NORTH, EAST],
            SOUTHEAST: [SOUTH, EAST],
            SOUTHWEST: [SOUTH, WEST],
            NORTHWEST: [NORTH, WEST],
        }
        return location2 in adjacent_map.get(location1, [])

    ### HELPERS ###
    def _is_arrow_movable(self, arrow: Arrow) -> bool:
        return (
            not arrow.is_dragging
            and arrow.motion
            and arrow.motion.motion_type != STATIC
        )

    def compare_states(self, current_state: Dict, candidate_state: Dict) -> bool:
        relevant_keys = [
            LETTER,
            START_POS,
            END_POS,
            BLUE_MOTION_TYPE,
            BLUE_PROP_ROT_DIR,
            BLUE_TURNS,
            BLUE_START_LOC,
            BLUE_END_LOC,
            RED_MOTION_TYPE,
            RED_PROP_ROT_DIR,
            RED_TURNS,
            RED_START_LOC,
            RED_END_LOC,
        ]
        return all(
            current_state.get(key) == candidate_state.get(key) for key in relevant_keys
        )

    # Function to get the Enum member key from a given letter
    def get_letter_type(self, letter: str) -> str | None:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return (
                    letter_type.name.replace("_", "").lower().capitalize()
                )  # Modify the key format
        return None
