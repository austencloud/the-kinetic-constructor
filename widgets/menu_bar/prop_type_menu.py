from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction, QActionGroup
from Enums.PropTypes import PropType
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QActionGroup, QAction

from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from widgets.menu_bar.main_window_menu_bar import MainWindowMenuBar



class PropTypeMenu(QMenu):
    def __init__(self, menu_bar: "MainWindowMenuBar"):
        super().__init__("Prop Type", menu_bar)
        self.menu_bar = menu_bar
        self.prop_type_selector = self.menu_bar.main_widget.prop_type_selector

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
        self.prop_type_selector.on_prop_type_changed(prop_type)
