from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from Enums.Enums import Letter  # Import the Letter enum

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class Lesson1PictographFactory:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.pictograph_cache = {}

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> BasePictograph:
        letter_str = pictograph_key.split("_")[0]

        # Convert the string to the Letter enum
        letter_enum = Letter.from_string(letter_str)

        if pictograph_key in self.pictograph_cache.get(letter_enum, {}):
            return self.pictograph_cache[letter_enum][pictograph_key]

        if pictograph_dict is not None:
            pictograph = self.create_pictograph(pictograph_dict)
            if letter_enum not in self.pictograph_cache:
                self.pictograph_cache[letter_enum] = {}
            self.pictograph_cache[letter_enum][pictograph_key] = pictograph
            return pictograph

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def create_pictograph(
        self, pictograph_dict
    ) -> BasePictograph:
        pictograph = BasePictograph(self.main_widget, scroll_area=None)
        pictograph.disable_gold_overlay = True
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph
