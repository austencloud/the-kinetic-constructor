# main_widget_tabs.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def on_tab_changed(self, index: int) -> None:
        tab_mapping = {
            self.main_widget.build_tab_index: (0, 0),
            self.main_widget.generate_tab_index: (0, 1),
            self.main_widget.dictionary_tab_index: (1, 0),
            self.main_widget.learn_tab_index: (1, 1),
            self.main_widget.act_tab_index: (2, None),
        }

        if index in tab_mapping:
            main_index, sub_index = tab_mapping[index]
            self.main_widget.main_stacked_widget.setCurrentIndex(main_index)
            if sub_index is not None:
                if main_index == 0:
                    self.main_widget.right_stacked_widget.setCurrentIndex(sub_index)
                elif main_index == 1:
                    self.main_widget.dictionary_learn_widget.setCurrentIndex(sub_index)

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

    def update_tab_based_on_settings(self) -> None:
        tab_indices = {
            "build": self.main_widget.build_tab_index,
            "generate": self.main_widget.generate_tab_index,
            "dictionary": self.main_widget.dictionary_tab_index,
            "learn": self.main_widget.learn_tab_index,
            "write": self.main_widget.act_tab_index,
        }

        if self.main_widget.current_tab in tab_indices:
            index = tab_indices[self.main_widget.current_tab]
            self.main_widget.navigation_widget.on_button_clicked(index)
            self.on_tab_changed(index)
