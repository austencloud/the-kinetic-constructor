from data.letter_types import letter_types
from objects.arrow.arrow import Arrow
from settings.string_constants import COLOR


class GraphboardInfoHandler:
    def __init__(self, main_widget, scene):
        self.main_widget = main_widget
        self.letters = main_widget.letters
        self.scene = scene

    def connect_widgets_and_managers(self):
        self.graph_editor = self.main_widget.graph_editor
        self.infobox = self.graph_editor.infobox
        self.staff_handler = self.scene.staff_handler
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_positioner = self.arrow_manager.positioner

    def update(self):
        self.arrow_positioner.update_arrow_position(self.arrow_manager.graphboard)
        self.infobox.labels.update_type_and_position_labels()
        self.scene.update_letter(self.determine_current_letter_and_type()[0])
        self.staff_handler.update_graphboard_staffs(self.scene)
        self.infobox.update()

    def determine_current_letter_and_type(self):
        current_combination = []
        arrowbox = self.main_widget.graph_editor.arrowbox

        # Check if an arrow is being dragged and add its attributes to the current_combination list
        if arrowbox.drag_preview == True:
            drag_attr = self.graphboard_drag_manager.drag_preview.get_attributes()
            sorted_drag_attr = {k: drag_attr[k] for k in sorted(drag_attr.keys())}
            current_combination.append(sorted_drag_attr)

        # Add attributes of arrows already in the scene to the current_combination list
        for arrow in self.scene.items():
            if isinstance(arrow, Arrow):
                attributes = arrow.attributes.get_attributes(arrow)
                sorted_attributes = {
                    k: attributes[k] for k in sorted(attributes.keys())
                }
                current_combination.append(sorted_attributes)

        # Sort the list of dictionaries by the 'color' key
        current_combination = sorted(current_combination, key=lambda x: x[COLOR])

        letter_type = None
        for letter, combinations in self.letters.items():
            combinations = [
                sorted([x for x in combination if COLOR in x], key=lambda x: x[COLOR])
                for combination in combinations
            ]
            if current_combination in combinations:
                self.letter = letter
                for (
                    type,
                    letters,
                ) in letter_types.items():  # Determine the type if a letter is found
                    if self.letter in letters:
                        current_type = type
                        break
                return self.letter, current_type  # Return both values here

        self.letter = None  # Set to None if no match is found
        return self.letter, letter_type  # Always return two values
