from objects.arrow import Arrow
from data import *
import json


class Letter_Manager():
    def __init__(self, artboard, info_tracker):
        self.artboard = artboard
        self.info_tracker = info_tracker
        self.letters = self.loadLetters()

    def __init__(self, artboard, info_tracker):
        self.artboard = artboard
        self.info_tracker = info_tracker
        self.letters = self.loadLetters()

    def loadLetters(self):
        try:
            with open('pictographs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def saveLetters(self):
        sorted_data = {key: self.letters[key] for key in sorted(self.letters)}
        with open('pictographs.json', 'w') as f:
            json.dump(sorted_data, f, indent=4)

    def assignLetter(self, letter):
        letter = letter.upper()
        if letter not in letter_positions:
            print(f"{letter} is not a valid letter.")
            return
        selected_items = self.artboard.selectedItems()
        if len(selected_items) != 2 or not all(isinstance(item, Arrow) for item in selected_items):
            print("Please select a combination of two arrows.")
            return
        letter_instance = Letter(selected_items[0], selected_items[1])
        letter_instance.assign_letter(letter)
        arrow_combination = [item.get_attributes() for item in selected_items]
        variations = generate_variations(arrow_combination)
        print(f"Generated {len(variations)} variations for the selected combination of arrows.")
        print(f"{variations}")
        if letter not in self.letters:
            self.letters[letter] = []
        for variation in variations:
            self.letters[letter].append(variation)
        self.letters[letter].sort(key=lambda x: (x[0]['color'], x[1]['color']))

        print(f"Assigned {letter} to the selected combination of arrows and all its variations.")
        self.info_tracker.update()

class Letter:
    def __init__(self, arrow1, arrow2):
        self.arrow1 = arrow1
        self.arrow2 = arrow2
        self.letter = None
        
    def get_start_location(self):
        start_location1 = Arrow.get_arrow_start_location(self.arrow1)
        start_location2 = Arrow.get_arrow_start_location(self.arrow2)
        print("start positions: ", start_location1, start_location2)

        return Arrow.get_position_from_directions(start_location1, start_location2)
        
    def get_end_location(self):
        end_location1 = Arrow.get_arrow_end_location(self.arrow1)
        end_location2 = Arrow.get_arrow_end_location(self.arrow2)
        print("end positions: ", end_location1, end_location2)


        return Arrow.get_position_from_directions(end_location1, end_location2)

    def assign_letter(self, letter):
        if (self.get_start_location(), self.get_end_location()) == letter_positions[letter]:
            self.letter = letter
            print(f"Assigned {letter} to the letter.")
        else:
            print(f"The start and end positions do not match the positions for {letter}.")

    def update_letter(self):
        current_combination = []

        for item in self.artboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)

        current_combination = sorted(current_combination, key=lambda x: x['color'])

        for letter, combinations in self.letters.items():
            combinations = [sorted(combination, key=lambda x: x['color']) for combination in combinations]
            if current_combination in combinations:
                return letter

        return None
