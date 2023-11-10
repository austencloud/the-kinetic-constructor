from settings.string_constants import ARROWS
from data.positions_map import positions_map
import cProfile
import pstats


class LetterEngine:
    def __init__(self, graphboard):
        self.graphboard = graphboard
        self.profiler = cProfile.Profile()
        
    def get_current_letter(self):
        self.profiler.enable() 
        current_combination, specific_position = self.get_specific_start_end_locations()
        possible_letters = self.get_possible_letters(specific_position)
        return self.get_match(current_combination, possible_letters)

    def get_specific_start_end_locations(self):
        start_locations, end_locations = self.get_start_end_locations_as_tuple()
        current_combination = self.graphboard.get_state()[ARROWS]
        specific_position = {
            "start_position": positions_map.get(start_locations),
            "end_position": positions_map.get(end_locations),
        }

        return current_combination, specific_position  # In case of no match

    def get_start_end_locations_as_tuple(self):
        self.red_arrow = (
            self.graphboard.arrows[0] if self.graphboard.arrows[0].color == "red" else self.graphboard.arrows[1]
        )
        self.blue_arrow = (
            self.graphboard.arrows[0] if self.graphboard.arrows[0].color == "blue" else self.graphboard.arrows[1]
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

    def get_motion_type(self):
        motion_type_group = {
            "pro_vs_pro": "ADGJMPS",
            "anti_vs_anti": "BEHKNQ",
            "pro_vs_anti": "CFILORUV",
            "static_vs_pro": "WYΣθ",
            "static_vs_anti": "XZΔΩ",
            "static_vs_static": "αβΓ"
        }
        red_motion_type = self.red_arrow.motion_type
        blue_motion_type = self.blue_arrow.motion_type

        combined_motion_type = None
        if red_motion_type == "pro" and blue_motion_type == "pro":
            combined_motion_type = "pro_vs_pro"
        elif red_motion_type == "anti" and blue_motion_type == "anti":
            combined_motion_type = "anti_vs_anti"
        elif red_motion_type == "pro" and blue_motion_type == "anti":
            combined_motion_type = "pro_vs_anti"
        elif red_motion_type == "static" and blue_motion_type == "pro":
            combined_motion_type = "static_vs_pro"
        elif red_motion_type == "static" and blue_motion_type == "anti":
            combined_motion_type = "static_vs_anti"
        elif red_motion_type == "static" and blue_motion_type == "static":
            combined_motion_type = "static_vs_static"
        
        return motion_type_group.get(combined_motion_type, "")

    def determine_parallel(self):
        # Define a set of parallel combinations
        parallel_combinations = {
            ('n', 'e', 'w', 's'), ('e', 's', 'n', 'w'),
            ('s', 'w', 'e', 'n'), ('w', 'n', 's', 'e'),
            ('n', 'w', 'e', 's'), ('w', 's', 'n', 'e'),
            ('s', 'e', 'w', 'n'), ('e', 'n', 's', 'w'),
        }

        # Get the start and end positions for both arrows
        red_start = self.red_arrow.start_location
        red_end = self.red_arrow.end_location
        blue_start = self.blue_arrow.start_location
        blue_end = self.blue_arrow.end_location

        # Check if the combination of start and end positions is in the set of parallel combinations
        return (red_start, red_end, blue_start, blue_end) in parallel_combinations

    def determine_handpath(self):
        clockwise = ['n', 'e', 's', 'w']

        red_start_index = clockwise.index(self.red_arrow.start_location)
        red_end_index = clockwise.index(self.red_arrow.end_location)
        blue_start_index = clockwise.index(self.blue_arrow.start_location)
        blue_end_index = clockwise.index(self.blue_arrow.end_location)

        red_direction = (red_end_index - red_start_index) % len(clockwise)
        blue_direction = (blue_end_index - blue_start_index) % len(clockwise)

        if red_direction == blue_direction:
            return 'same'
        else:
            return 'opp'

    def get_gamma_handpath_group(self):
        gamma_handpath_group = {
            "opp": "MNOPQR",
            "same": "STUV",
        }
        handpath_type = self.determine_handpath()
        return gamma_handpath_group.get(handpath_type, "")

    def get_gamma_opp_handpath_group(self):
        if self.determine_parallel():
            return "MNO"  # Return the group of letters corresponding to parallel motion
        else:
            return "PQR"  # Return the group of letters corresponding to antiparallel motion

    def determine_same_handpath_hybrid(self):
        # Define the clockwise and counterclockwise directions
        clockwise = ['n', 'e', 's', 'w']
        counterclockwise = ['n', 'w', 's', 'e']

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

        red_direction_ccw = (red_start_index_ccw - red_end_index_cw) % len(counterclockwise)
        blue_direction_ccw = (blue_start_index_ccw - blue_end_index_cw) % len(counterclockwise)

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
            if red_start_index_ccw == (blue_start_index_ccw + 1) % len(counterclockwise):
                # Red is leading counterclockwise
                return "leading_" + self.red_arrow.motion_type
            elif blue_start_index_ccw == (red_start_index_ccw + 1) % len(counterclockwise):
                # Blue is leading counterclockwise
                return "leading_" + self.blue_arrow.motion_type

        # If they're not moving in the same rotational direction or not leading/following directly, we don't have a hybrid
        return ""

    def get_gamma_same_handpath_hybrid_group(self):
        gamma_same_handpath_hybrid_group = {
            "leading_pro": "U",
            "leading_anti": "V",
        }

        same_handpath_hybrid_type = self.determine_same_handpath_hybrid()
        return gamma_same_handpath_hybrid_group.get(same_handpath_hybrid_type, "")

    def get_possible_letters(self, specific_position):
        if specific_position["start_position"] and specific_position["end_position"]:
            overall_position = self.get_overall_position(specific_position)
            possible_letters = self.get_letter_group(overall_position)
            motion_possible_letters = set(self.get_motion_type())
            possible_letters = {
                letter: combinations
                for letter, combinations in possible_letters.items()
                if letter in motion_possible_letters
            }

            # If the end position belongs to the gamma group, apply the gamma handpath logic
            if 'gamma' in overall_position.get('end_position', '').lower():
                gamma_handpath_letters = set(self.get_gamma_handpath_group())
                possible_letters = {
                    letter: combinations
                    for letter, combinations in possible_letters.items()
                    if letter in gamma_handpath_letters
                }

                # Apply the opp/same handpath logic
                if any(letter in 'MNOPQR' for letter in possible_letters):
                    gamma_opp_handpath_letters = set(self.get_gamma_opp_handpath_group())
                    possible_letters = {
                        letter: combinations
                        for letter, combinations in possible_letters.items()
                        if letter in gamma_opp_handpath_letters
                    }

                if any(letter in 'STUV' for letter in possible_letters):
                    gamma_same_handpath_hybrid_letters = set(self.get_gamma_same_handpath_hybrid_group())
                    possible_letters = {
                        letter: combinations
                        for letter, combinations in possible_letters.items()
                        if letter in gamma_same_handpath_hybrid_letters
                    }

        return possible_letters

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
            possible_letters = set(end_category).intersection(start_category)

            return {
                letter: combinations
                for letter, combinations in self.graphboard.letters.items()
                if letter in possible_letters
            }
        return {}

    def get_match(self, current_combination, possible_letters):
        for letter, combinations in possible_letters.items():
            self.profiler.enable()
            for combination in combinations:
                if self.match_combination(current_combination, combination):
                    self.letter = letter
                    self.profiler.disable()
                    self.write_profiling_stats_to_file("letter_engine_stats.txt")
                    return letter

    def match_combination(self, current_combination, combination):
        # Pre-fetch values outside of the loop to avoid repeated dictionary lookups
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
                if all(pre_fetched_arrow.get(key, None) == comb.get(key, None) for key in pre_fetched_arrow):
                    current_arrows_matched[i] = True
                    break
                    
        return all(current_arrows_matched)



    def write_profiling_stats_to_file(self, file_path):
        stats = pstats.Stats(self.profiler).sort_stats('cumtime')
        with open(file_path, "w") as f:
            stats.stream = f
            stats.print_stats()
        print(f"Letter engine profiling stats written to {file_path}")