from typing import Any, Dict, List, Tuple

from settings.string_constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    EAST,
    END_POS,
    NORTH,
    location,
    ROTATION_DIRECTION,
    SOUTH,
    START_POS,
    WEST,
)
from utilities.TypeChecking.TypeChecking import (
    Locations,
    Locations,
    RotationDirections,
    MotionAttributesDicts,
)


class JsonVariationsGenerator:
    def __init__(self) -> None:
        self.location_mapping: Dict[Tuple[Locations, Locations], str] = {}
        for start in [NORTH, SOUTH]:
            for end in [EAST, WEST]:
                self.location_mapping[(start, end)] = f"{start}{end}"

    def calculate_location(
        self, start_location: Locations, end_location: Locations
    ) -> Locations:
        return self.location_mapping.get((start_location, end_location))

    def apply_mapping(
        self,
        arrow_combination: List[MotionAttributesDicts],
        position_mapping: Dict[Locations, Locations],
        rotation_mapping: Dict[RotationDirections, RotationDirections],
    ) -> List[MotionAttributesDicts]:
        return [
            {
                **arrow,
                START_POS: position_mapping[arrow[START_POS]],
                END_POS: position_mapping[arrow[END_POS]],
                ROTATION_DIRECTION: rotation_mapping[arrow[ROTATION_DIRECTION]],
                **self.calculate_location(
                    position_mapping[arrow[START_POS]],
                    position_mapping[arrow[END_POS]],
                ),
            }
            for arrow in arrow_combination
        ]

    def generate_pictograph_variants(
        self, arrow_combination: List[MotionAttributesDicts]
    ) -> List[Dict[str, Any]]:
        rotation_mapping: Dict[Locations, Locations] = {
            NORTH: EAST,
            EAST: SOUTH,
            SOUTH: WEST,
            WEST: NORTH,
        }
        vertical_reflection_mapping: Dict[Locations, Locations] = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: EAST,
            WEST: WEST,
        }
        horizontal_reflection_mapping: Dict[Locations, Locations] = {
            NORTH: NORTH,
            SOUTH: SOUTH,
            EAST: WEST,
            WEST: EAST,
        }
        rotation_reflection_mapping: Dict[RotationDirections, RotationDirections] = {
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
