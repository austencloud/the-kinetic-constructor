import random

class TurnIntensityManager:
    def __init__(self, max_turns: int, word_length: int, level: int, max_turn_intensity: float):
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
        self.turns_allocated = [0] * word_length  # Initialize turn allocation to zero for each motion.
        self.possible_turns = self._get_possible_turns()

    def _get_possible_turns(self):
        """Return a list of valid turns based on the level."""
        if self.level == 2:
            # Whole numbers for level 2
            return [0, 1, 2, 3]
        else:
            # Half steps for level 3
            return [0, 0.5, 1, 1.5, 2, 2.5, 3]

    def allocate_turns(self):
        """
        Allocate turns across the sequence without exceeding max_turns, ensuring that
        no individual turn exceeds max_turn_intensity, and only valid turns are used.
        """
        remaining_turns = self.max_turns  # Total turns that can be distributed

        # Filter the possible turns to only those that don't exceed the max_turn_intensity
        valid_turns = [turn for turn in self.possible_turns if turn <= self.max_turn_intensity]

        # Distribute turns across each motion within the word length
        for i in range(self.word_length):
            if remaining_turns <= 0:
                break

            # Randomly select a valid turn that does not exceed the remaining turns
            turn_value = random.choice([t for t in valid_turns if t <= remaining_turns])

            # Store the allocated turn and reduce the remaining turns
            self.turns_allocated[i] = turn_value
            remaining_turns -= turn_value

        return self.turns_allocated
