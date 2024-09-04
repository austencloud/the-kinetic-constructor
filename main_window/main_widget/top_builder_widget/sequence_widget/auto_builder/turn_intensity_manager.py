import random


class TurnIntensityManager:
    def __init__(self, max_turns: int, sequence_length: int, level: int):
        self.max_turns = max_turns
        self.sequence_length = sequence_length
        self.remaining_turns = max_turns
        self.level = level

    def allocate_turns(self) -> list[float]:
        """Allocate turns across the sequence considering the remaining turns."""
        turns = []
        for _ in range(self.sequence_length):
            if self.remaining_turns > 0:
                # Choose available turns based on the sequence level
                if self.level == 2:
                    possible_turns = [0, 1, 2, 3]  # Whole numbers only
                else:
                    possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]

                turn = random.choice(possible_turns)
                if turn > self.remaining_turns:
                    turn = self.remaining_turns
                self.remaining_turns -= turn
            else:
                turn = 0
            turns.append(turn)
        return turns
