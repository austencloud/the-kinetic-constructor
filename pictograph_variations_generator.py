class PictographVariationsGenerator:
    def __init__(self):
        self.quadrant_mapping = {}
        for start in ['n', 's']:
            for end in ['e', 'w']:
                self.quadrant_mapping[(start, end)] = f"{start}{end}"

    def calculate_quadrant(self, start_position, end_position):
        return self.quadrant_mapping.get((start_position, end_position))

    def apply_mapping(self, arrow_combination, position_mapping, rotation_mapping):
        return [{**arrow,
                 "start_position": position_mapping[arrow["start_position"]],
                 "end_position": position_mapping[arrow["end_position"]],
                 "rotation": rotation_mapping[arrow["rotation"]],
                 "quadrant": self.calculate_quadrant(
                     position_mapping[arrow["start_position"]],
                     position_mapping[arrow["end_position"]])}
                for arrow in arrow_combination]

    def generate_pictograph_variations(self, arrow_combination):
        rotation_mapping = {"n": "e", "e": "s", "s": "w", "w": "n"}
        vertical_reflection_mapping = {"n": "s", "s": "n", "e": "e", "w": "w"}
        horizontal_reflection_mapping = {"n": "n", "s": "s", "e": "w", "w": "e"}
        rotation_reflection_mapping = {"l": "r", "r": "l"}

        rotated_versions = [arrow_combination]
        for _ in range(3):
            arrow_combination = self.apply_mapping(
                arrow_combination, rotation_mapping, rotation_reflection_mapping)
            rotated_versions.append(arrow_combination)

        reflected_versions = []
        for version in rotated_versions:
            vertical_reflected_version = self.apply_mapping(
                version, vertical_reflection_mapping, rotation_reflection_mapping)
            horizontal_reflected_version = self.apply_mapping(
                version, horizontal_reflection_mapping, rotation_reflection_mapping)
            reflected_versions.extend(
                [vertical_reflected_version, horizontal_reflected_version])

        return rotated_versions + reflected_versions
