# main_widget_tabs.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def on_tab_changed(self, index: int) -> None:
        tab_actions = {
            self.main_widget.build_tab_index: (
                "build",
                self.main_widget.manual_builder.resize_manual_builder,
            ),
            self.main_widget.generate_tab_index: (
                "generate",
                self.main_widget.sequence_generator.resize_sequence_generator,
            ),
            self.main_widget.dictionary_tab_index: (
                "dictionary",
                self.main_widget.dictionary_widget.resize_dictionary_widget,
            ),
            self.main_widget.learn_tab_index: (
                "learn",
                self.main_widget.learn_widget.resize_learn_widget,
            ),
        }

        if index in [
            self.main_widget.build_tab_index,
            self.main_widget.generate_tab_index,
        ]:
            self.main_widget.sequence_widget.show()
        else:
            self.main_widget.sequence_widget.hide()

        self.main_widget.stacked_widget.setCurrentIndex(index)
        self.main_widget.content_layout.setStretch(0, 1)
        self.main_widget.content_layout.setStretch(1, 1)

        if index in tab_actions:
            tab_name, action = tab_actions[index]
            self.main_widget.settings_manager.global_settings.set_current_tab(tab_name)
            action()
            if (
                index == self.main_widget.dictionary_tab_index
                and not self.main_widget.dictionary_widget.initialized
            ):
                self.main_widget.dictionary_widget.initialized = True
                self.main_widget.dictionary_widget.resize_dictionary_widget()

    def update_tab_based_on_settings(self) -> None:
        tab_indices = {
            "build": self.main_widget.build_tab_index,
            "generate": self.main_widget.generate_tab_index,
            "dictionary": self.main_widget.dictionary_tab_index,
            "learn": self.main_widget.learn_tab_index,
        }

        if self.main_widget.current_tab in tab_indices:
            index = tab_indices[self.main_widget.current_tab]
            self.main_widget.navigation_widget.on_button_clicked(index)
            self.main_widget.stacked_widget.setCurrentIndex(index)



