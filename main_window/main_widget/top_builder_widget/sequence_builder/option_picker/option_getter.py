from typing import TYPE_CHECKING
from data.constants import END_POS, START_POS

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionGetter:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.json_manager = self.option_picker.json_manager
        self.main_widget = self.option_picker.main_widget

    def get_next_options(self, sequence: list, filters: dict):
        # Load all possible next options based on the current sequence
        all_next_options = self._load_all_next_options(sequence)

        # Apply filters to the options
        filtered_options = self._apply_filters(all_next_options, filters)

        return filtered_options

    def _load_all_next_options(self, sequence: list):
        # Logic to load all possible next options based on the current sequence
        # This would typically involve analyzing the last pictograph and determining valid next steps
        # For now, let's assume it returns a list of pictograph dictionaries
        next_options = []

        last_pictograph_dict = (
            sequence[-1]
            if sequence[-1].get("is_placeholder", "") != True
            else sequence[-2]
        )
        start_pos = last_pictograph_dict[END_POS]

        if start_pos:
            for dict_list in self.main_widget.pictograph_dicts.values():
                for dict in dict_list:
                    if dict[START_POS] == start_pos:
                        next_options.append(dict)
        return next_options

    def _apply_filters(self, options: list, filters: dict):
        # Filters:
        # - continuous_motions: Include motions that are continuous
        # - prop_reversals: Include motions that involve prop reversals
        # - hand_reversals: Include motions that involve hand reversals

        filtered_options = []

        for pictograph_dict in options:
            include_pictograph = True

            # Check for continuous motions
            if not filters["continuous_motions"]:
                if self._is_continuous_motion(pictograph_dict):
                    include_pictograph = False

            # Check for prop reversals
            if not filters["prop_reversals"]:
                if self._is_prop_reversal(pictograph_dict):
                    include_pictograph = False

            # Check for hand reversals
            if not filters["hand_reversals"]:
                if self._is_hand_reversal(pictograph_dict):
                    include_pictograph = False

            if include_pictograph:
                filtered_options.append(pictograph_dict)

        return filtered_options

    def _is_continuous_motion(self, pictograph_dict: dict) -> bool:
        # Logic to determine if a pictograph represents a continuous motion
        # This would be based on properties within the pictograph_dict
        return pictograph_dict.get("is_continuous", False)

    def _is_prop_reversal(self, pictograph_dict: dict) -> bool:
        # Logic to determine if a pictograph involves a prop reversal
        return pictograph_dict.get("is_prop_reversal", False)

    def _is_hand_reversal(self, pictograph_dict: dict) -> bool:
        # Logic to determine if a pictograph involves a hand reversal
        return pictograph_dict.get("is_hand_reversal", False)
