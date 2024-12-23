# main_widget_tabs.py

import logging
from typing import TYPE_CHECKING, Optional, Callable

from PyQt6.QtCore import QObject, pyqtSlot

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabsHandler(QObject):
    """
    Handles tab-switch logic, referencing the TabFadeManager for fade animations.
    Manages transitions between primary tabs and coordinates internal transitions within BuildTab.
    """

    def __init__(self, main_widget: "MainWidget"):
        """
        Initialize MainWidgetTabs.

        Args:
            main_widget (MainWidget): Reference to the main widget containing all components.
        """
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Connect navigation signals to tab switching slots
        self.logger.debug(
            "MainWidgetTabs initialized and connected to navigation signals."
        )

    @pyqtSlot(int)
    def on_tab_selected(self, tab_index: int):
        """
        Handle tab selection from navigation.

        Args:
            tab_index (int): Index of the selected tab from the navigation widget.
        """
        mw = self.main_widget

        # Define the mapping from navigation index to main_stacked_widget index
        # Navigation Indices:
        # 0 → Construct
        # 0 → Generate
        # 1 → Browse
        # 2 → Learn
        # 3 → Write

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
            self.main_widget.fade_manager.fade_to_tab(main_stack_index)

            if tab_name == "construct":
                self.main_widget.build_tab.show_build()
            elif tab_name == "generate":
                self.main_widget.build_tab.show_generate()
        else:
            self.main_widget.fade_manager.fade_to_tab(main_stack_index)

    def update_tab_based_on_settings(self) -> None:
        """
        Switch to the tab indicated by saved settings.
        This method should be called during application startup to restore the last selected tab.
        """
        mw = self.main_widget
        current_tab_name = mw.settings_manager.global_settings.get_current_tab()

        # Define the mapping from tab names to navigation indices
        tab_indices = {
            "construct": mw.construct_tab_index,
            "generate": mw.generate_tab_index,
            "browse": mw.browse_tab_index,
            "learn": mw.learn_tab_index,
            "write": mw.write_tab_index,
        }

        if current_tab_name in tab_indices:
            nav_index = tab_indices[current_tab_name]
            self.logger.debug(f"Emitting tab_selected signal with index: {nav_index}")
            self.main_widget.navigation_widget.tab_selected.emit(nav_index)
        else:
            self.logger.warning(
                f"Unknown tab name in settings: {current_tab_name}. Defaulting to Build."
            )
            # Default to Build tab if the saved tab is unknown
            self.main_widget.navigation_widget.tab_selected.emit(mw.build_tab_index)
