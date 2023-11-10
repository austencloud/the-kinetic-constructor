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

    def get_possible_letters(self, specific_position):
        if specific_position["start_position"] and specific_position["end_position"]:
            overall_position = self.get_overall_position(specific_position)
            possible_letters = self.get_letter_group(overall_position)
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
            for combination in combinations:
                if self.match_combination(current_combination, combination):
                    self.letter = letter
                    self.profiler.disable()
                    return letter
            self.write_profiling_stats_to_file("letter_engine_stats.txt")

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