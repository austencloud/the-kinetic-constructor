class JsonVariationsGenerator:
    def __init__(self):
        self.quadrant_mapping = {}
        for start in [NORTH, SOUTH]:
            for end in [EAST, WEST]:
                self.quadrant_mapping[(start, end)] = f"{start}{end}"

    def calculate_quadrant(self, start_position, end_position):
        return self.quadrant_mapping.get((start_position, end_position))

    def apply_mapping(self, arrow_combination, position_mapping, rotation_mapping):
        return [
            {
                **arrow,
                START_POS: position_mapping[arrow[START_POS]],
                END_POS: position_mapping[arrow[END_POS]],
                "rotation": rotation_mapping[arrow["rotation"]],
                QUADRANT: self.calculate_quadrant(
                    position_mapping[arrow[START_POS]],
                    position_mapping[arrow[END_POS]],
                ),
            }
            for arrow in arrow_combination
        ]

    def generate_pictograph_variants(self, arrow_combination):
        rotation_mapping = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}
        vertical_reflection_mapping = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: EAST,
            WEST: WEST,
        }
        horizontal_reflection_mapping = {
            NORTH: NORTH,
            SOUTH: SOUTH,
            EAST: WEST,
            WEST: EAST,
        }
        rotation_reflection_mapping = {
            COUNTER_CLOCKWISE: CLOCKWISE,
            CLOCKWISE: COUNTER_CLOCKWISE,
        }

        rotated_versions = [arrow_combination]
        for _ in range(3):
            arrow_combination = self.apply_mapping(
                arrow_combination, rotation_mapping, rotation_reflection_mapping
            )
            rotated_versions.append(arrow_combination)

        reflected_versions = []
        for version in rotated_versions:
            vertical_reflected_version = self.apply_mapping(
                version, vertical_reflection_mapping, rotation_reflection_mapping
            )
            horizontal_reflected_version = self.apply_mapping(
                version, horizontal_reflection_mapping, rotation_reflection_mapping
            )
            reflected_versions.extend(
                [vertical_reflected_version, horizontal_reflected_version]
            )

        return rotated_versions + reflected_versions
