import json
import os
from objects.arrow import Arrow
from PyQt6.QtCore import QObject

class Json_Manager(QObject):
    def __init__(self, scene):
        self.scene = scene
        self.letters = self.load_all_letters()

    def load_all_letters(self):
        directory = 'json\\'
        letters = {}
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r',  encoding='utf-8') as file:
                    letter_data = json.load(file)
                    letter_key = filename.replace('.json', '')
                    letters[letter_key] = letter_data[letter_key]
        return letters

    def update_individual_json(self, letter, updated_data, directory):
        filepath = os.path.join(directory, f"{letter}.json")
        with open(filepath, 'w') as file:
            # Wrap the updated data in a dictionary with the letter as the key
            json.dump({letter: updated_data}, file, indent=4)


    def update_optimal_locations_in_json(self, red_position, blue_position):
        current_attributes = []
        updated_letters = []  # Keep track of updated letters

        for item in self.scene.items():
            if isinstance(item, Arrow):
                current_attributes.append(item.get_attributes())
        current_attributes = sorted(current_attributes, key=lambda x: x['color'])

        for letter, combinations in self.letters.items():
            for i, combination_set in enumerate(combinations):
                arrow_attributes = [d for d in combination_set if 'color' in d]
                combination_attributes = sorted(arrow_attributes, key=lambda x: x['color'])

                if combination_attributes == current_attributes:
                    new_optimal_red = {'x': red_position.x(), 'y': red_position.y()}
                    new_optimal_blue = {'x': blue_position.x(), 'y': blue_position.y()}
                    new_optimal_positions = {
                        "optimal_red_location": new_optimal_red,
                        "optimal_blue_location": new_optimal_blue
                    }

                    optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
                    if optimal_positions is not None:
                        optimal_positions.update(new_optimal_positions)
                        print(f"Updated optimal positions for letter {letter}")
                    else:
                        combination_set.append(new_optimal_positions)
                        print(f"Added optimal positions for letter {letter}")

                    if letter not in updated_letters:
                        updated_letters.append(letter)

        # Update individual JSON files for each updated letter
        for letter in updated_letters:
            self.update_individual_json(letter, self.letters[letter], 'json\\')  # Update the specific JSON file
