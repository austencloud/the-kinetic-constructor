from typing import TYPE_CHECKING
from data.constants import END_POS, START_POS

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionGetter:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.json_manager = self.option_picker.json_manager
        self.main_widget = self.option_picker.main_widget

    def get_next_options(self, sequence: list, selected_filter: str) -> list:
        # Load all possible next options based on the current sequence
        all_next_options = self._load_all_next_options(sequence)

        # Apply filter to the options
        filtered_options = self._apply_filter(
            sequence, all_next_options, selected_filter
        )

        #change the start ori of the next options to reflect the end ori of the last pictograph
        for option in filtered_options:
            option["blue_attributes"]["start_ori"] = sequence[-1]["blue_attributes"]["end_ori"]
            option["red_attributes"]["start_ori"] = sequence[-1]["red_attributes"]["end_ori"]
            
            
        # use the motion ori calculator to determine that end ori of the motion and set it to that. 
        for option in filtered_options:
            option["blue_attributes"]["end_ori"] = self.json_manager.ori_calculator.calculate_end_orientation(option, "blue")
            option["red_attributes"]["end_ori"] = self.json_manager.ori_calculator.calculate_end_orientation(option, "red")
            
        return filtered_options

    def _apply_filter(self, sequence: list, options: list, selected_filter: str):
        filtered_options = []

        for pictograph_dict in options:
            # Include options based on the selected filter
            if selected_filter is None:
                # "All" selected, include all options
                filtered_options.append(pictograph_dict)
                continue

            # Implement your existing logic to categorize pictographs
            category = self._determine_category(sequence, pictograph_dict)

            if category == selected_filter:
                filtered_options.append(pictograph_dict)

        return filtered_options

    def _determine_category(self, sequence: list, pictograph_dict: dict) -> str:

        # Proceed with continuity checks
        blue_continuous, red_continuous = self._check_continuity(
            sequence, pictograph_dict
        )

        # Determine the category
        if blue_continuous and red_continuous:
            category = "continuous"
        elif (blue_continuous and not red_continuous) or (
            not blue_continuous and red_continuous
        ):
            category = "one_reversal"
        else:
            category = "two_reversals"
        return category

    def _load_all_next_options(self, sequence: list) -> list:
        # Logic to load all possible next options based on the current sequence
        # This involves analyzing the last pictograph and determining valid next steps
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
                        
        # we need to get the end orientation of the last item in the sequence and set the start otientations of 
        # each next option to it, then use the JsonOrientationValidationEngine to validate and update the new end ori for each option
        for option in next_options:
            option["blue_attributes"]["start_ori"] = last_pictograph_dict["blue_attributes"]["end_ori"]
            option["red_attributes"]["start_ori"] = last_pictograph_dict["red_attributes"]["end_ori"]
            self.json_manager.ori_validation_engine.validate_single_pictograph(
                option, last_pictograph_dict
            )
                        
        return next_options

    def _apply_filters(self, sequence: list, options: list, filters: dict):
        filtered_options = []

        for pictograph_dict in options:
            # Check if both prop_rot_dir are "no_rot"
            blue_prop_rot_dir = pictograph_dict["blue_attributes"]["prop_rot_dir"]
            red_prop_rot_dir = pictograph_dict["red_attributes"]["prop_rot_dir"]
            if blue_prop_rot_dir == "no_rot" and red_prop_rot_dir == "no_rot":
                # Always include pictographs with both prop_rot_dir as "no_rot"
                filtered_options.append(pictograph_dict)
                continue  # Skip further checks

            # Proceed with continuity checks
            blue_continuous, red_continuous = self._check_continuity(
                sequence, pictograph_dict
            )

            # Determine the category
            if blue_continuous and red_continuous:
                category = "continuous"
            elif (blue_continuous and not red_continuous) or (
                not blue_continuous and red_continuous
            ):
                category = "one_reversal"
            else:
                category = "two_reversals"

            # Include pictograph if its category is selected in filters
            include_pictograph = False
            if filters.get("continuous") and category == "continuous":
                include_pictograph = True
            elif filters.get("one_reversal") and category == "one_reversal":
                include_pictograph = True
            elif filters.get("two_reversals") and category == "two_reversals":
                include_pictograph = True

            if include_pictograph:
                filtered_options.append(pictograph_dict)

        return filtered_options

    def _check_continuity(self, sequence: list, pictograph_dict: dict):
        last_blue_dir = self._get_last_prop_rot_dir(sequence[1:], "blue")
        last_red_dir = self._get_last_prop_rot_dir(sequence[1:], "red")

        current_blue_dir = pictograph_dict["blue_attributes"]["prop_rot_dir"]
        current_red_dir = pictograph_dict["red_attributes"]["prop_rot_dir"]

        # For "no_rot", use last known direction
        if current_blue_dir == "no_rot":
            current_blue_dir = last_blue_dir
        if current_red_dir == "no_rot":
            current_red_dir = last_red_dir

        # If still None, consider continuous
        if last_blue_dir is None or current_blue_dir is None:
            blue_continuous = True
        else:
            blue_continuous = current_blue_dir == last_blue_dir

        if last_red_dir is None or current_red_dir is None:
            red_continuous = True
        else:
            red_continuous = current_red_dir == last_red_dir

        return blue_continuous, red_continuous

    def _get_last_prop_rot_dir(self, sequence: list, color: str) -> str:
        # color should be "blue" or "red"
        for pictograph in reversed(sequence):
            prop_rot_dir = pictograph[f"{color}_attributes"].get("prop_rot_dir")
            if prop_rot_dir != "no_rot":
                return prop_rot_dir
        return None  # No previous direction found
