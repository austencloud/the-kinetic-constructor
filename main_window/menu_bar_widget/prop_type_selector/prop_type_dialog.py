# prop_type_dialog.py
from Enums.PropTypes import PropType
from typing import TYPE_CHECKING
from ..options_dialog import OptionsDialog

if TYPE_CHECKING:
    from .prop_type_selector import PropTypeSelector


class PropTypeDialog:
    def __init__(self, prop_type_selector: "PropTypeSelector"):
        self.prop_type_selector = prop_type_selector
        self.prop_types = [
            PropType.Hand,
            PropType.Staff,
            PropType.Club,
            PropType.Fan,
            PropType.Triad,
            PropType.Minihoop,
            PropType.Buugeng,
            PropType.Sword,
            PropType.Ukulele,
        ]
        self.options = [prop_type.name for prop_type in self.prop_types]

    def show_dialog(self):
        dialog = OptionsDialog(
            selector=self.prop_type_selector,
            options=self.options,
            callback=self.option_selected,
        )
        dialog.show_dialog(self.prop_type_selector.label)

    def option_selected(self, option_name: str):
        prop_type = PropType[option_name]
        self.prop_type_selector.set_current_prop_type(prop_type)
