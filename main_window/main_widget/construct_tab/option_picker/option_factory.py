from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from .option_view import OptionView

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

class OptionFactory:
    MAX_PICTOGRAPHS = 36

    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.main_widget = option_picker.main_widget
        self.create_options()

    def create_options(self) -> list[BasePictograph]:
        options = []
        for _ in range(self.MAX_PICTOGRAPHS):
            option = BasePictograph(self.main_widget)
            option.view = OptionView(self.option_picker, option)
            options.append(option)
        self.option_picker.option_pool = options
