from typing import Any, Dict, List, Tuple

from settings.string_constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    EAST,
    END_POS,
    NORTH,
    QUADRANT,
    ROTATION_DIRECTION,
    SOUTH,
    START_POS,
    WEST,
)
from utilities.TypeChecking.TypeChecking import (
    Location,
    Quadrant,
    RotationDirection,
    MotionAttributesDicts,
)


class JsonVariationsGenerator:
    def __init__(self) -> None:
        self.quadrant_mapping: Dict[Tuple[Location, Location], str] = {}
        for start in [NORTH, SOUTH]:
            for end in [EAST, WEST]:
                self.quadrant_mapping[(start, end)] = f"{start}{end}"

    def calculate_quadrant(
        self, start_location: Location, end_location: Location
    ) -> Quadrant:
        return self.quadrant_mapping.get((start_location, end_location))

    def apply_mapping(
        self,
        arrow_combination: Dict[Location, Location],
        position_mapping: Dict[Location, Location],
        rotation_mapping: Dict[RotationDirection, RotationDirection],
    ) -> List[MotionAttributesDicts]:
        return [
            {
                **arrow,
                START_POS: position_mapping[arrow[START_POS]],
                END_POS: position_mapping[arrow[END_POS]],
                ROTATION_DIRECTION: rotation_mapping[arrow[ROTATION_DIRECTION]],
                QUADRANT: self.calculate_quadrant(
                    position_mapping[arrow[START_POS]],
                    position_mapping[arrow[END_POS]],
                ),
            }
            for arrow in arrow_combination
        ]

    def generate_pictograph_variants(
        self, arrow_combination: List[MotionAttributesDicts]
    ) -> List[Dict[str, Any]]:
        rotation_mapping: Dict[Location, Location] = {
            NORTH: EAST,
            EAST: SOUTH,
            SOUTH: WEST,
            WEST: NORTH,
        }
        vertical_reflection_mapping: Dict[Location, Location] = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: EAST,
            WEST: WEST,
        }
        horizontal_reflection_mapping: Dict[Location, Location] = {
            NORTH: NORTH,
            SOUTH: SOUTH,
            EAST: WEST,
            WEST: EAST,
        }
        rotation_reflection_mapping: Dict[RotationDirection, RotationDirection] = {
            COUNTER_CLOCKWISE: CLOCKWISE,
            CLOCKWISE: COUNTER_CLOCKWISE,
        }

        rotated_variants = [arrow_combination]
        for _ in range(3):
            arrow_combination = self.apply_mapping(
                arrow_combination, rotation_mapping, rotation_reflection_mapping
            )
            rotated_variants.append(arrow_combination)

        reflected_variants: List[List[MotionAttributesDicts]] = []
        for variant in rotated_variants:
            vertical_reflected_variant = self.apply_mapping(
                variant, vertical_reflection_mapping, rotation_reflection_mapping
            )
            horizontal_reflected_variant = self.apply_mapping(
                variant, horizontal_reflection_mapping, rotation_reflection_mapping
            )
            reflected_variants.extend(
                [vertical_reflected_variant, horizontal_reflected_variant]
            )

        return rotated_variants + reflected_variants
