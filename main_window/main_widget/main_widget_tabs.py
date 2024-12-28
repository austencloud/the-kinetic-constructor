from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    """Handles tab-switch logic, referencing the TabFadeManager for fade animations."""

    def __init__(self, main_widget: "MainWidget"):
        """Initialize MainWidgetTabs."""
        self.mw = main_widget

    def on_tab_changed(self, index: int) -> None:
        tab_names = {
            self.mw.construct_tab_index: "build",
            self.mw.generate_tab_index: "generate",
            self.mw.browse_tab_index: "browse",
            self.mw.learn_tab_index: "learn",
            self.mw.write_tab_index: "write",
        }
        if index in tab_names:
            self.mw.settings_manager.global_settings.set_current_tab(tab_names[index])

        self.mw.stack_fade_manager.fade_to_tab(self.mw.right_stack, index)
        QApplication.processEvents()
        if index == self.mw.learn_tab_index:
            self.mw.stack_fade_manager.fade_to_tab(self.mw.left_stack, 1)
        else:
            self.mw.stack_fade_manager.fade_to_tab(self.mw.left_stack, 0)

    def update_tab_based_on_settings(self) -> None:
        """Switch to the tab indicated by saved settings."""
        tab_indices = {
            "build": self.mw.construct_tab_index,
            "generate": self.mw.generate_tab_index,
            "browse": self.mw.browse_tab_index,
            "learn": self.mw.learn_tab_index,
            "write": self.mw.write_tab_index,
        }
        current_tab_name = self.mw.current_tab
        if current_tab_name in tab_indices:
            idx = tab_indices[current_tab_name]
            self.mw.navigation_widget.on_button_clicked(idx)
            self.on_tab_changed(idx)
