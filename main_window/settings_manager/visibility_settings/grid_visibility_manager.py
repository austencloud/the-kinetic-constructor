from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )


class GridVisibilityManager:
    def __init__(self, visibility_settings: "VisibilitySettings") -> None:
        self.visibility_settings = visibility_settings
        self.settings_manager = visibility_settings.settings_manager
        self.non_radial_visible = self.visibility_settings.get_grid_visibility(
            "non_radial_points"
        )

    def save_non_radial_visibility(self, visible: bool):
        self.visibility_settings.set_grid_visibility("non_radial_points", visible)
        self.apply_visibility_to_all_pictographs()

    def set_non_radial_visibility(self, visible: bool):
        self.non_radial_visible = visible
        self.save_non_radial_visibility(visible)

    def toggle_visibility(self):
        self.non_radial_visible = not self.non_radial_visible
        self.save_non_radial_visibility(self.non_radial_visible)

    def apply_visibility_to_all_pictographs(self):
        # Apply non-radial visibility to all pictographs in the application
        main_widget = self.settings_manager.main_window.main_widget
        for pictograph_list in main_widget.pictograph_cache.values():
            for start_pos in pictograph_list.values():
                if hasattr(start_pos, "grid"):
                    start_pos.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        for option in main_widget.construct_tab.option_picker.option_pool:
            if hasattr(option, "grid"):
                option.grid.toggle_non_radial_points_visibility(self.non_radial_visible)

        # Apply visibility to additional views
        beat_frame = main_widget.sequence_widget.beat_frame
        for beat_view in beat_frame.beats:
            if hasattr(beat_view, "beat"):
                if hasattr(beat_view, "beat") and hasattr(beat_view.beat, "grid"):
                    beat_view.beat.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        start_pos_view = beat_frame.start_pos_view
        if start_pos_view.isVisible():
            start_pos = start_pos_view.beat
            if hasattr(start_pos, "grid"):
                start_pos.grid.toggle_non_radial_points_visibility(
                    self.non_radial_visible
                )

        # Apply to advanced start pos picker and the GE blank pictograph
        construct_tab = main_widget.construct_tab
        for (
            pictograph_list
        ) in construct_tab.advanced_start_pos_picker.start_pos_cache.values():
            for start_pos in pictograph_list:
                if hasattr(start_pos, "grid"):
                    start_pos.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        graph_editor = main_widget.sequence_widget.graph_editor
        GE_blank_pictograph = (
            graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )
        if hasattr(GE_blank_pictograph, "grid"):
            GE_blank_pictograph.grid.toggle_non_radial_points_visibility(
                self.non_radial_visible
            )
