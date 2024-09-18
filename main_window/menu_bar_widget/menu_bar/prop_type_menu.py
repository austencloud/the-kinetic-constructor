from PyQt6.QtGui import QAction, QActionGroup
from Enums.PropTypes import PropType
from typing import TYPE_CHECKING

from .hoverable_menu import HoverableMenu

if TYPE_CHECKING:
    from .menu_bar import MenuBar


class PropTypeMenu(HoverableMenu):
    def __init__(self, menu_bar: "MenuBar"):
        super().__init__("Prop Type", menu_bar)
        self.menu_bar = menu_bar
        self.settings_manager = self.menu_bar.main_widget.main_window.settings_manager
        self.prop_type_changer = self.settings_manager.global_settings.prop_type_changer

        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)

        for prop_type in [
            PropType.Hand,
            PropType.Staff,
            PropType.Club,
            PropType.Fan,
            PropType.Triad,
            PropType.Minihoop,
            PropType.Buugeng,
            PropType.Sword,
            PropType.Ukulele,
        ]:
            action = QAction(prop_type.name, self, checkable=True)
            action.triggered.connect(
                lambda checked, pt=prop_type: self.set_prop_type(pt)
            )
            self.addAction(action)
            prop_type_action_group.addAction(action)

            if self.menu_bar.main_widget.prop_type == prop_type:
                action.setChecked(True)

    def set_prop_type(self, prop_type: PropType):
        self.on_prop_type_changed(prop_type)

    def on_prop_type_changed(self, new_prop_type: PropType) -> None:
        self.settings_manager.global_settings.set_prop_type(new_prop_type)
        self.settings_manager.save_settings()
        self.prop_type_changer.apply_prop_type()
