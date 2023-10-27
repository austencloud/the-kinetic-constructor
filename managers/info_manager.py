from data.letter_types import letter_types
from objects.arrow.arrow import Arrow

class GraphboardInfoManager():
    def __init__(self, main_widget, view):
        self.main_widget = main_widget
        self.letters = main_widget.letters
        self.view = view


    def connect_widgets_and_managers(self):
        self.graph_editor_widget = self.main_widget.graph_editor_widget
        self.info_frame = self.graph_editor_widget.info_frame
        self.staff_manager = self.view.staff_manager
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_positioner = self.arrow_manager.arrow_positioner
        
    def update(self):
        self.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard_view)
        self.info_frame.update_type_and_position_info()
        self.view.update_letter(self.determine_current_letter_and_type()[0])
        self.staff_manager.update_graphboard_staffs(self.view.scene())

    def connect_view(self, view):
        self.view = view
        
    def determine_current_letter_and_type(self):
        current_combination = []
        for arrow in self.view.items():
            if isinstance(arrow, Arrow):
                attributes = arrow.attributes.get_attributes(arrow)
                sorted_attributes = {k: attributes[k] for k in sorted(attributes.keys())}
                current_combination.append(sorted_attributes)
        # Sort the list of dictionaries by the 'color' key
        current_combination = sorted(current_combination, key=lambda x: x['color'])
        letter_type = None
        for letter, combinations in self.letters.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]
            if current_combination in combinations:
                self.letter = letter
                for type, letters in letter_types.items():  # Determine the type if a letter is found
                    if self.letter in letters:
                        current_type = type
                        break
                return self.letter, current_type  # Return both values here
        self.letter = None  # Set to None if no match is found

        return self.letter, letter_type  # Always return two values