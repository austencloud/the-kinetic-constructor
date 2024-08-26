from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction, QActionGroup
from Enums.PropTypes import PropType
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QActionGroup, QAction

from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBar


class PropTypeMenu(QMenu):
    def __init__(self, menu_bar: "MenuBar"):
        super().__init__("Prop Type", menu_bar)
        self.menu_bar = menu_bar
        self.settings_manager = self.menu_bar.main_widget.main_window.settings_manager
        self.prop_type_selector = self.menu_bar.main_widget.prop_type_selector
        self.prop_type_changer = self.menu_bar.main_widget.main_window.settings_manager.global_settings.prop_type_changer
        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)

        for prop_type in PropType:
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

