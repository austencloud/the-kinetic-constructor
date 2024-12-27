import random


class TurnIntensityManager:
    def __init__(self, word_length: int, level: int, max_turn_intensity: float):
        """
        Initialize the TurnIntensityManager with:
        - max_turns: The maximum number of total turns that can be applied.
        - word_length: The number of motions (or beats) in the sequence.
        - level: The level which determines valid turn values (Level 2 or Level 3).
        - max_turn_intensity: The maximum number of turns allowed for any single motion.
        """
        self.word_length = word_length
        self.level = level
        self.max_turn_intensity = max_turn_intensity
        self.turns_allocated = [
            0
        ] * word_length  # Initialize turn allocation to zero for each motion.
        self.turns_allocated_blue = [0] * word_length  # Blue motion turns
        self.turns_allocated_red = [0] * word_length  # Red motion turns

    def allocate_turns_for_blue_and_red(self):
        if self.level == 2:
            possible_turns = [0, 1, 2, 3]
        elif self.level == 3:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]
        else:
            possible_turns = [0]  # For other levels, default to no turns

        for i in range(self.word_length):
            # For blue
            turn_blue = random.choice(
                [
                    t
                    for t in possible_turns
                    if t == "fl"
                    or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
                ]
            )
            self.turns_allocated_blue[i] = turn_blue

            # For red
            turn_red = random.choice(
                [
                    t
                    for t in possible_turns
                    if t == "fl"
                    or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
                ]
            )
            self.turns_allocated_red[i] = turn_red

        return self.turns_allocated_blue, self.turns_allocated_red
