import json
import os
from arrow import Arrow


class Mini_Json_Manager:
    def __init__(self, mini_graphboard_scene):
        self.mini_graphboard_scene = mini_graphboard_scene
        

    def update_optimal_locations_in_json(self, red_position, blue_position):
        with open('pictographs.json', 'r') as file:
            data = json.load(file)
        current_attributes = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                current_attributes.append(item.get_attributes())
        current_attributes = sorted(current_attributes, key=lambda x: x['color'])

        print("Current attributes:", current_attributes)

        for letter, combinations in data.items():
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
        with open('pictographs.json', 'w') as file:
            json.dump(data, file, indent=4)

class Json_Manager:
    def __init__(self, graphboard_scene):
        self.graphboard_scene = graphboard_scene

    def update_optimal_locations_in_json(self, red_position, blue_position):
        with open('pictographs.json', 'r') as file:
            data = json.load(file)
        current_attributes = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                current_attributes.append(item.get_attributes())
        current_attributes = sorted(current_attributes, key=lambda x: x['color'])

        print("Current attributes:", current_attributes)

        for letter, combinations in data.items():
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
        with open('pictographs.json', 'w') as file:
            json.dump(data, file, indent=4)
