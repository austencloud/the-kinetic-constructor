from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    """Handles tab-switch logic, referencing the TabFadeManager for fade animations."""

    def __init__(self, main_widget: "MainWidget"):
        """Initialize MainWidgetTabs."""
        self.main_widget = main_widget

        # Create the fade manager for the main_stacked_widget
        # (or pass in an existing TabFadeManager if you already made it in main_widget)

    def on_tab_changed(self, index: int) -> None:
        tab_names = {
            self.main_widget.build_tab_index: "build",
            self.main_widget.generate_tab_index: "generate",
            self.main_widget.dictionary_tab_index: "dictionary",
            self.main_widget.learn_tab_index: "learn",
            self.main_widget.act_tab_index: "write",
        }
        if index in tab_names:
            self.main_widget.settings_manager.global_settings.set_current_tab(
                tab_names[index]
            )

        self.main_widget.fade_manager.fade_to_tab(
            self.main_widget.content_stack, index
        )


    def update_tab_based_on_settings(self) -> None:
        """Switch to the tab indicated by saved settings."""
        tab_indices = {
            "build": self.main_widget.build_tab_index,
            "generate": self.main_widget.generate_tab_index,
            "dictionary": self.main_widget.dictionary_tab_index,
            "learn": self.main_widget.learn_tab_index,
            "write": self.main_widget.act_tab_index,
        }
        current_tab_name = self.main_widget.current_tab
        if current_tab_name in tab_indices:
            idx = tab_indices[current_tab_name]
            # Possibly update navigation widget
            self.main_widget.navigation_widget.on_button_clicked(idx)
            self.on_tab_changed(idx)
