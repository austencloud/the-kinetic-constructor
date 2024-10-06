# prop_type_selector.py
from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from ..base_selector import LabelSelector
from .prop_type_dialog import PropTypeDialog

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class PropTypeSelector(LabelSelector):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        self.main_widget = menu_bar_widget.main_window.main_widget
        current_prop_type = self.main_widget.prop_type.name
        super().__init__(menu_bar_widget, current_prop_type)
        self.settings_manager = self.main_window.settings_manager
        self.prop_type_changer = self.settings_manager.global_settings.prop_type_changer

    def on_label_clicked(self):
        dialog = PropTypeDialog(self)
        dialog.show_dialog()

    def set_current_prop_type(self, prop_type: PropType):
        self.set_display_text(prop_type.name)
        self.settings_manager.global_settings.set_prop_type(prop_type)
        self.settings_manager.save_settings()
        self.prop_type_changer.apply_prop_type()
