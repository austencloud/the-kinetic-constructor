# main_widget_tabs.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainWidgetTabs:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def on_tab_changed(self, index: int) -> None:
        if index in [
            self.main_widget.build_tab_index,
            self.main_widget.generate_tab_index,
        ]:
            self.main_widget.sequence_widget.setVisible(True)
        else:
            self.main_widget.sequence_widget.setVisible(False)

        self.main_widget.stacked_widget.setCurrentIndex(index)

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
