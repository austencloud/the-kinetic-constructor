# main_widget_tab_switcher.py

from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtCore import QObject, pyqtSlot

from main_window.main_widget.fade_manager import FadeManager


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabSwitcher(QObject):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_stack = self.main_widget.main_stacked_widget

        # Initialize UnifiedFadeManager

        # Connect navigation signals to tab switching slots
        self.main_widget.navigation_widget.tab_changed.connect(self.on_tab_selected)

    @pyqtSlot(int, int)
    def on_tab_selected(self, tab_index: int, previous_index: int) -> None:
        tab_mapping = {
            0: ("construct", 0),  # BuildTab's SequenceConstructor
            1: ("generate", 0),  # BuildTab's SequenceGeneratorWidget
            2: ("dictionary", 1),  # DictionaryTab
            3: ("learn", 2),  # LearnTab
            4: ("write", 3),  # ActTab
        }

        if tab_index not in tab_mapping:
            return

        tab_name, new_main_index = tab_mapping[tab_index]
        self.main_widget.settings_manager.global_settings.set_current_tab(tab_name)

        if tab_name in ["construct", "generate"]:
            new_build_index = 0 if tab_name == "construct" else 1

            # Determine if we're switching within the build tab
            if (
                self.main_stack.currentIndex() == new_main_index
                and self.main_widget.build_tab.build_stacked_widget.currentIndex()
                == new_build_index
            ):
                return  # No change needed

            # Use the unified fade manager to handle both main and build transitions
            self.main_widget.fade_manager.fade_to_tabs(
                new_main_index=new_main_index, new_build_index=new_build_index
            )
        else:
            # For other primary tabs, fade only the main stack
            self.main_widget.fade_manager.fade_to_tabs(
                new_main_index=new_main_index, new_build_index=None
            )
