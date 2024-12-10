# base_pictograph.py


from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PlaceholderPictograph(BasePictograph):
    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.pictograph_dict = {
            "letter": "Unknown",
            "start_pos": "unknown",
            "end_pos": "unknown",
            "timing": "none",
            "direction": "none",
            "letter_type": "Unknown",
            "blue_attributes": {},
            "red_attributes": {},
        }
        self.letter_type = None  # or set to a default LetterType

        self.updater.update_pictograph(self.pictograph_dict)
