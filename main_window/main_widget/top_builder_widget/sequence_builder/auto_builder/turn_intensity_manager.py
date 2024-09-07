import random


class TurnIntensityManager:
    def __init__(
        self, max_turns: int, word_length: int, level: int, max_turn_intensity: float
    ):
        """
        Initialize the TurnIntensityManager with:
        - max_turns: The maximum number of total turns that can be applied.
        - word_length: The number of motions (or beats) in the sequence.
        - level: The level which determines valid turn values (Level 2 or Level 3).
        - max_turn_intensity: The maximum number of turns allowed for any single motion.
        """
        self.max_turns = max_turns
        self.word_length = word_length
        self.level = level
        self.max_turn_intensity = max_turn_intensity
        self.turns_allocated = [
            0
        ] * word_length  # Initialize turn allocation to zero for each motion.
        self.turns_allocated_blue = [0] * word_length  # Blue motion turns
        self.turns_allocated_red = [0] * word_length  # Red motion turns

    def allocate_turns_for_blue_and_red(self):
        """
        Allocate separate turns for blue and red attributes across the sequence without exceeding max_turns,
        ensuring that no individual turn exceeds max_turn_intensity.
        """
        remaining_turns_blue = self.max_turns
        remaining_turns_red = self.max_turns

        # Define valid turn options for level
        if self.level == 2:
            possible_turns = [0, 1, 2, 3]  # Whole numbers only
        else:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]

        # Distribute turns across each motion for blue and red within the word length
        for i in range(self.word_length):
            if remaining_turns_blue <= 0 and remaining_turns_red <= 0:
                break

            # Allocate turns for blue motion
            max_turn_blue = min(self.max_turn_intensity, remaining_turns_blue)
            turn_blue = random.choice([t for t in possible_turns if t <= max_turn_blue])
            self.turns_allocated_blue[i] = turn_blue
            remaining_turns_blue -= turn_blue

            # Allocate turns for red motion
            max_turn_red = min(self.max_turn_intensity, remaining_turns_red)
            turn_red = random.choice([t for t in possible_turns if t <= max_turn_red])
            self.turns_allocated_red[i] = turn_red
            remaining_turns_red -= turn_red

        return self.turns_allocated_blue, self.turns_allocated_red
