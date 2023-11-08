from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from data.positions_map import positions_map
from data.letter_types import letter_types
class Letter(QGraphicsSvgItem):
    def __init__(self, graphboard):
        self.graphboard = graphboard
        super().__init__()

    def get_current_letter(self):
        start_end_positions = self.get_start_end_positions()

        specific_position = positions_map.get(start_end_positions)

        if specific_position:
            overall_position = self.get_overall_position(specific_position)
            possible_letters = self.get_possible_letters(overall_position)
            for letter, combinations in possible_letters.items():
                if self.current_combination in combinations:
                    self.graphboard.letter = letter
                    return self.graphboard.letter

        self.graphboard.letter = None
        return self.graphboard.letter

    def get_start_end_positions(self):
        # get the red arrow from the arrows array, ensure that it's red with a check
        for arrow in self.graphboard.arrows:
            if arrow.color == 'red':
                red_arrow_index = self.graphboard.arrows.index(arrow)
            if arrow.color == 'blue':
                blue_arrow_index = self.graphboard.arrows.index(arrow)
        
        start_positions = (self.graphboard.arrows[red_arrow_index].start_location, 'red', self.graphboard.arrows[blue_arrow_index].start_location, 'blue')
        end_positions = (self.graphboard.arrows[red_arrow_index].end_location, 'red', self.graphboard.arrows[blue_arrow_index].end_location, 'blue')
        return start_positions + end_positions

    def get_overall_position(self, graphboard, specific_position):
        # Logic to convert specific position to overall position
        return specific_position[:-1]

    def get_possible_letters(self, graphboard, overall_position):
        # Logic to return only the letters that begin with the overall position
        category_map = {
            'alpha': 'ABC',
            'beta': 'DEF',
            'gamma': 'MNOPQRSTUV',
            # Add other categories as needed
        }
        category = category_map.get(overall_position)
        if category:
            return {letter: combinations for letter, combinations in self.graphboard.letters.items() if letter.startswith(category)}
        return {}

    def get_current_letter_type(self):
        letter = self.get_current_letter()
        if letter is not None:
            for letter_type, letters in letter_types.items():
                if letter in letters:
                    return letter_type
        else:
            return None
