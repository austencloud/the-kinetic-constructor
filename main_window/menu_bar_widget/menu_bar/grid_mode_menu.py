from PyQt6.QtGui import QAction
from typing import TYPE_CHECKING
from data.constants import BOX, DIAMOND
from .hoverable_menu import HoverableMenu
from main_window.main_widget.top_builder_widget.sequence_widget.graph_editor.GE_pictograph_view import (
    GE_BlankPictograph,
)

if TYPE_CHECKING:
    from .menu_bar import MenuBar


class GridModeMenu(HoverableMenu):
    def __init__(self, menu_bar: "MenuBar"):
        super().__init__("Grid Mode", menu_bar)
        self.menu_bar = menu_bar
        self.main_widget = self.menu_bar.main_widget
        for grid_mode in ["Diamond", "Box"]:
            action = QAction(f"{grid_mode}", self, checkable=True)
            action.triggered.connect(
                lambda checked, grid_mode=grid_mode: self.toggle_grid_mode(grid_mode)
            )
            self.addAction(action)

        current_grid_mode = (
            self.main_widget.main_window.settings_manager.global_settings.get_grid_mode()
        )
        self.toggle_selected_grid_mode(current_grid_mode.capitalize())

    def toggle_selected_grid_mode(self, grid_mode):
        for action in self.actions():
            if action.text() == grid_mode:
                action.setChecked(True)
            else:
                action.setChecked(False)

    def toggle_grid_mode(self, grid_mode: str):
        self.toggle_selected_grid_mode(grid_mode)
        self.main_widget.main_window.settings_manager.global_settings.set_grid_mode(
            grid_mode.lower()
        )
        self.main_widget.main_window.settings_manager.save_settings()
        self.main_widget.grid_mode = grid_mode.lower()
        self.main_widget.pictograph_dicts = (
            self.main_widget.pictograph_dict_loader.load_all_pictograph_dicts()
        )

        start_pos_manager = (
            self.main_widget.top_builder_widget.sequence_builder.manual_builder.start_pos_picker.start_pos_manager
        )
        start_pos_manager.clear_start_positions()
        start_pos_manager.setup_start_positions()
        # start_pos_manager.start_pos_picker.resize_start_pos_picker()

        sequence_clearer = (
            self.main_widget.top_builder_widget.sequence_widget.sequence_clearer
        )
        sequence_clearer.clear_sequence()

        pictograph_container = (
            self.main_widget.top_builder_widget.sequence_widget.graph_editor.pictograph_container
        )
        pictograph_container.GE_pictograph_view.blank_pictograph = GE_BlankPictograph(
            pictograph_container
        )
        pictograph_container.GE_pictograph_view.set_to_blank_grid()
