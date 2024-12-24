# main_widget_tabs.py

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSlot

from main_window.main_widget.tab_fade_manager import TabFadeManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabsHandler(QObject):
    """
    Handles tab-switch logic, referencing the TabFadeManager for fade animations.
    Manages transitions between primary tabs and coordinates internal transitions within BuildTab.
    """

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.fade_manager = TabFadeManager(self)

    @pyqtSlot(int)
    def on_tab_selected(self, tab_index: int):
        tab_mapping = {
            0: ("construct", 0),
            1: ("generate", 0),
            2: ("browse", 1),
            3: ("learn", 2),
            4: ("write", 3),
        }

        if tab_index not in tab_mapping:
            return

        tab_name, main_stack_index = tab_mapping[tab_index]
        self.main_widget.settings_manager.global_settings.set_current_tab(tab_name)

        if tab_name in ["construct", "generate"]:
            self.fade_manager.fade_to_tab(main_stack_index)

            if tab_name == "construct":
                self.main_widget.build_tab.show_construct()
            elif tab_name == "generate":
                self.main_widget.build_tab.show_generate()
        else:
            self.fade_manager.fade_to_tab(main_stack_index)
