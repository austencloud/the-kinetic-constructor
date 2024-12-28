from turtle import left
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    """Handles tab-switch logic, referencing the TabFadeManager for fade animations."""

    def __init__(self, main_widget: "MainWidget"):
        """Initialize MainWidgetTabs."""
        self.mw = main_widget

    def on_tab_changed(self, index: int) -> None:
        if (
            index == self.mw.learn_tab_index
            and self.mw.right_stack.currentIndex() == index
        ):
            return
        right_new_index = None
        if index == self.mw.learn_tab_index:
            left_new_index = 1
            self.mw.left_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
            self.mw.right_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
        elif index == self.mw.write_tab_index:
            left_new_index = 2
            self.mw.left_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
            self.mw.right_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
        elif index == self.mw.browse_tab_index:
            left_new_index = 3
            right_new_index = 2
            self.mw.left_stack.setMaximumWidth(int(self.mw.width() * 2 / 3))
            self.mw.right_stack.setMaximumWidth(int(self.mw.width() * 1 / 3))
        elif index == self.mw.generate_tab_index:
            left_new_index = 0
            self.mw.left_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
            self.mw.right_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
        elif index == self.mw.construct_tab_index:
            left_new_index = 0
            self.mw.left_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))
            self.mw.right_stack.setMaximumWidth(int(self.mw.width() * 1 / 2))

        if (
            index in [self.mw.generate_tab_index, self.mw.construct_tab_index]
            and self.mw.left_stack.currentIndex() == 0
        ):
            new_index = 1 if index == self.mw.generate_tab_index else 0
            self.mw.stack_fade_manager.fade_to_tab(
                stack=self.mw.right_stack, new_index=new_index
            )
        else:
            if not right_new_index:
                right_new_index = index
            self.mw.stack_fade_manager.fade_both_stacks_in_parallel(
                right_stack=self.mw.right_stack,
                right_new_index=right_new_index,
                left_stack=self.mw.left_stack,
                left_new_index=left_new_index,
            )

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
