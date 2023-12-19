from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph

from widgets.option_picker.option.option_view import OptionView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker.option_picker import OptionPicker


class Option(Pictograph):
    def __init__(
        self,
        main_widget: "MainWidget",
        option_picker: "OptionPicker",
        is_starter: bool = False,  # Set a default value for is_starter
    ) -> None:
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.is_starter = is_starter
        self.option_picker: OptionPicker = option_picker
        self.setup_scene()
        self.setup_components(self.main_widget)
        self.view = OptionView(self)

    ### UPDATERS ###

    def wheelEvent(self, event) -> None:
        return super().wheelEvent(event)
