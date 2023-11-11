from settings.string_constants import ARROWS
from data.positions_map import positions_map
import logging

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class LetterEngine:
    def __init__(self, graphboard):
        self.graphboard = graphboard
        self.preprocessed_combinations = self.preprocess_combinations(
            graphboard.letters
        )
        self.motion_type_letter_groups = None
        self.cached_parallel = None
        self.cached_handpath = None

    def preprocess_combinations(self, letters):
        # Pre-process the letter groups for each start/end position and motion type
        preprocessed = {}
        for letter, combinations in letters.items():
            for combination in combinations:
                start_pos = combination[0].get("start_position")
                end_pos = combination[0].get("end_position")
                if start_pos and end_pos:
                    key = (start_pos, end_pos)
                    preprocessed.setdefault(key, []).append((letter, combination[1:]))
        return preprocessed

    def get_arrow(self, color):
        return next(
            (arrow for arrow in self.graphboard.arrows if arrow.color == color), None
        )

    def get_current_combination(self):
        return self.graphboard.get_state()[ARROWS]

    def get_specific_start_end_positions(self):
        red_arrow = self.get_arrow("red")
        blue_arrow = self.get_arrow("blue")

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

        specific_position = {
            "start_position": positions_map.get(start_locations),
            "end_position": positions_map.get(end_locations),
        }

        self.red_arrow = red_arrow
        self.blue_arrow = blue_arrow
        return specific_position

    def get_start_end_locations_as_tuple(self):
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

        return start_locations, end_locations

    def get_motion_type_letter_group(self):
        if self.motion_type_letter_groups is None:
            self.motion_type_letter_groups = {
                "pro_vs_pro": "ADGJMPS",
                "anti_vs_anti": "BEHKNQT",
                "pro_vs_anti": "CFILORUV",
                "static_vs_pro": "WYΣθ",
                "static_vs_anti": "XZΔΩ",
                "static_vs_static": "αβΓ",
            }

        red_motion_type = self.red_arrow.motion_type
        blue_motion_type = self.blue_arrow.motion_type
        combined_motion_type = None

        ### NON_HYBRIDS ###

        if red_motion_type == "pro" and blue_motion_type == "pro":
            combined_motion_type = "pro_vs_pro"
        elif red_motion_type == "anti" and blue_motion_type == "anti":
            combined_motion_type = "anti_vs_anti"
        elif red_motion_type == "static" and blue_motion_type == "static":
            combined_motion_type = "static_vs_static"
            
        ### HYBRIDS ###
            
        elif red_motion_type == "pro" and blue_motion_type == "anti":
            combined_motion_type = "pro_vs_anti"
        elif red_motion_type == "anti" and blue_motion_type == "pro":
            combined_motion_type = "pro_vs_anti"
        elif red_motion_type == "static" and blue_motion_type == "pro":
            combined_motion_type = "static_vs_pro"
        elif red_motion_type == "pro" and blue_motion_type == "static":
            combined_motion_type = "static_vs_pro"
        elif red_motion_type == "static" and blue_motion_type == "anti":
            combined_motion_type = "static_vs_anti"
        elif red_motion_type == "anti" and blue_motion_type == "static":
            combined_motion_type = "static_vs_anti"


        motion_type_letter_group = self.motion_type_letter_groups.get(
            combined_motion_type, ""
        )
        
        self.combined_motion_type = combined_motion_type
        self.motion_letter_group = motion_type_letter_group
        
        return motion_type_letter_group

    def determine_parallel(self):
        parallel_combinations = {
            ("n", "e", "w", "s"),
            ("e", "s", "n", "w"),
            ("s", "w", "e", "n"),
            ("w", "n", "s", "e"),
            ("n", "w", "e", "s"),
            ("w", "s", "n", "e"),
            ("s", "e", "w", "n"),
            ("e", "n", "s", "w"),
        }

        red_start = self.red_arrow.start_location
        red_end = self.red_arrow.end_location
        blue_start = self.blue_arrow.start_location
        blue_end = self.blue_arrow.end_location

        self.cached_parallel = (
            red_start,
            red_end,
            blue_start,
            blue_end,
        ) in parallel_combinations

        return self.cached_parallel

    def determine_handpath(self):
        clockwise = ["n", "e", "s", "w"]

        red_start_index = clockwise.index(self.red_arrow.start_location)
        red_end_index = clockwise.index(self.red_arrow.end_location)
        blue_start_index = clockwise.index(self.blue_arrow.start_location)
        blue_end_index = clockwise.index(self.blue_arrow.end_location)

        red_direction = (red_end_index - red_start_index) % len(clockwise)
        blue_direction = (blue_end_index - blue_start_index) % len(clockwise)

        cached_handpath = "same" if red_direction == blue_direction else "opp"

        self.cached_handpath = cached_handpath
        return cached_handpath

    def get_gamma_handpath_group(self):
        gamma_handpath_group = {
            "opp": "MNOPQR",
            "same": "STUV",
        }
        handpath_type = self.determine_handpath()
        return gamma_handpath_group.get(handpath_type, "")

    def get_gamma_opp_handpath_letter_group(self):
        if self.determine_parallel():
            return "MNO"  # Return the group of letters corresponding to parallel motion
        else:
            return "PQR"  # Return the group of letters corresponding to antiparallel motion

    def determine_same_handpath_hybrid(self):  #
        # Define the clockwise and counterclockwise directions
        clockwise = ["n", "e", "s", "w"]
        counterclockwise = ["n", "w", "s", "e"]

        # Get the start and end positions for both arrows
        red_start = self.red_arrow.start_location
        red_end = self.red_arrow.end_location
        blue_start = self.blue_arrow.start_location
        blue_end = self.blue_arrow.end_location

        # Find the index in the clockwise and counterclockwise directions
        red_start_index_cw = clockwise.index(red_start)
        red_end_index_cw = clockwise.index(red_end)
        blue_start_index_cw = clockwise.index(blue_start)
        blue_end_index_cw = clockwise.index(blue_end)

        red_start_index_ccw = counterclockwise.index(red_start)
        blue_start_index_ccw = counterclockwise.index(blue_start)

        # Determine if both arrows are moving in the same rotational direction (clockwise or counterclockwise)
        red_direction_cw = (red_end_index_cw - red_start_index_cw) % len(clockwise)
        blue_direction_cw = (blue_end_index_cw - blue_start_index_cw) % len(clockwise)

        red_direction_ccw = (red_start_index_ccw - red_end_index_cw) % len(
            counterclockwise
        )
        blue_direction_ccw = (blue_start_index_ccw - blue_end_index_cw) % len(
            counterclockwise
        )

        if red_direction_cw == blue_direction_cw:
            # Both arrows are moving clockwise
            if red_start_index_cw == (blue_start_index_cw + 1) % len(clockwise):
                # Red is leading clockwise
                return "leading_" + self.red_arrow.motion_type
            elif blue_start_index_cw == (red_start_index_cw + 1) % len(clockwise):
                # Blue is leading clockwise
                return "leading_" + self.blue_arrow.motion_type

        elif red_direction_ccw == blue_direction_ccw:
            # Both arrows are moving counterclockwise
            if red_start_index_ccw == (blue_start_index_ccw + 1) % len(
                counterclockwise
            ):
                # Red is leading counterclockwise
                return "leading_" + self.red_arrow.motion_type
            elif blue_start_index_ccw == (red_start_index_ccw + 1) % len(
                counterclockwise
            ):
                # Blue is leading counterclockwise
                return "leading_" + self.blue_arrow.motion_type

        # If they're not moving in the same rotational direction or not leading/following directly, we don't have a hybrid
        return ""

    def get_gamma_same_handpath_hybrid_letter(self):
        gamma_same_handpath_hybrid_group = {
            "leading_pro": "U",
            "leading_anti": "V",
        }

        same_handpath_hybrid_type = self.determine_same_handpath_hybrid()
        gamma_same_handpath_hybrid_letter = gamma_same_handpath_hybrid_group.get(
            same_handpath_hybrid_type, ""
        )
        # convert the letter to a string

        return gamma_same_handpath_hybrid_letter

    def get_current_letter(self):
        specific_position = self.get_specific_start_end_positions()
        overall_position = self.get_overall_position(specific_position)
        letter_group = self.get_letter_group(overall_position)
        motion_letter_group = set(self.get_motion_type_letter_group())

        # Filter letter group based on motion letter group
        filtered_letter_group = {
            letter: combinations
            for letter, combinations in letter_group.items()
            if letter in motion_letter_group
        }

        if "gamma" in overall_position.get("end_position", "").lower():
            filtered_letter_group = self.get_gamma_letter(filtered_letter_group)

        # Return the current letter
        if len(filtered_letter_group) == 1:
            current_letter = list(filtered_letter_group.keys())[0]
            return current_letter
        else:
            logging.debug(
                "Multiple letters returned by get_current_letter: %s",
                filtered_letter_group,
            )
            return None

    def get_gamma_letter(self, letter_group):
        gamma_handpath_letters = set(self.get_gamma_handpath_group())
        filtered_letter_group = {
            letter: combinations
            for letter, combinations in letter_group.items()
            if letter in gamma_handpath_letters
        }

        # Opp/same handpath logic
        if any(letter in "MNOPQR" for letter in filtered_letter_group):
            gamma_opp_handpath_letters = set(self.get_gamma_opp_handpath_letter_group())
            filtered_letter_group = {
                letter: combinations
                for letter, combinations in filtered_letter_group.items()
                if letter in gamma_opp_handpath_letters
            }

        if any(letter in "STUV" for letter in filtered_letter_group):
            if self.combined_motion_type == "pro_vs_anti":
                gamma_same_handpath_hybrid_letter = (
                    self.get_gamma_same_handpath_hybrid_letter()
                )
                filtered_letter_group = {
                    letter: combinations
                    for letter, combinations in filtered_letter_group.items()
                    if letter == gamma_same_handpath_hybrid_letter
                }

        return filtered_letter_group

    def get_current_letter_dict(self, current_letter):
        overall_position = self.get_overall_position(self.specific_position)
        letter_group = self.get_letter_group(overall_position)
        motion_letter_group = set(self.get_motion_type_letter_group())
        filtered_letter_group = {
            letter: combinations
            for letter, combinations in letter_group.items()
            if letter == current_letter and letter in motion_letter_group
        }

        return filtered_letter_group.get(current_letter, [])

    def get_overall_position(self, specific_positions):
        return {position: value[:-1] for position, value in specific_positions.items()}

    def get_letter_group(self, overall_position):
        end_group = {
            "alpha": "ABCDEFWXα",
            "beta": "GHIJKLYZβ",
            "gamma": "MNOPQRSTUVΣΔθΩΓ",
        }
        start_group = {
            "alpha": "ABCJKLΣΔα",
            "beta": "GHIDEFθΩβ",
            "gamma": "MNOPQRSTUVWXYZΓ",
        }

        end_category = end_group.get(overall_position.get("end_position"))
        start_category = start_group.get(overall_position.get("start_position"))

        if end_category and start_category:
            # Intersect the sets to get only the letters that are in both start and end groups
            letter_group = set(end_category).intersection(start_category)

            return {
                letter: combinations
                for letter, combinations in self.graphboard.letters.items()
                if letter in letter_group
            }
        return {}

    def match_combination(self, current_combination, current_letter, combination):
        pre_fetched_current_combination = [
            {key: arrow.get(key, None) for key in arrow}
            for arrow in current_combination
        ]

        current_arrows_matched = [False] * len(current_combination)
        for comb in combination:
            # Skip if 'start_position' or 'end_position' are not in 'comb'
            if "start_position" in comb and "end_position" in comb:
                continue

            for i, pre_fetched_arrow in enumerate(pre_fetched_current_combination):
                if current_arrows_matched[i]:
                    continue
                # Compare pre-fetched values instead of accessing them from the dictionary
                if all(
                    pre_fetched_arrow.get(key, None) == comb.get(key, None)
                    for key in pre_fetched_arrow
                ):
                    current_arrows_matched[i] = True
                    break

        return all(current_arrows_matched)