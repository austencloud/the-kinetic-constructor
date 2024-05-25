from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager import SettingsManager


class GridVisibilityManager:
    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.non_radial_visible = self.load_visibility_settings()

    def load_visibility_settings(self) -> bool:
        return self.settings_manager.get_setting("non_radial_points_visibility", True)

    def save_visibility_settings(self):
        self.settings_manager.set_setting(
            "non_radial_points_visibility", self.non_radial_visible
        )
        self.settings_manager.save_settings()

    def toggle_visibility(self):
        self.non_radial_visible = not self.non_radial_visible
        self.save_visibility_settings()
        self.apply_visibility_to_all_pictographs()

    def apply_visibility_to_all_pictographs(self):
        for (
            pictograph_list
        ) in self.settings_manager.main_window.main_widget.pictograph_cache.values():
            for start_pos in pictograph_list.values():
                if hasattr(start_pos, "grid"):
                    start_pos.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )
        # iterate over the sequence widget beat frame too
        beat_frame = (
            self.settings_manager.main_window.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        for beat_view in beat_frame.beats:
            if hasattr(beat_view, "beat"):
                beat = beat_view.beat
                if hasattr(beat, "grid"):
                    beat.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        # if the start pos view is visible, apply the visibility to it too
        start_pos_view = beat_frame.start_pos_view
        if start_pos_view.isVisible():
            start_pos = start_pos_view.beat
            if hasattr(start_pos, "grid"):
                start_pos.grid.toggle_non_radial_points_visibility(
                    self.non_radial_visible
                )

        # iterate over the advanced start pos picker pictographs too
        sequence_builder = (
            self.settings_manager.main_window.main_widget.top_builder_widget.sequence_builder
        )
        for (
            start_letter,
            pictograph_list,
        ) in sequence_builder.advanced_start_pos_picker.start_pos_cache.items():
            for start_pos in pictograph_list:
                if hasattr(start_pos, "grid"):
                    start_pos.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        # apply the change to the GE_BlankPictograph too
        self.main_widget = self.settings_manager.main_window.main_widget
        graph_editor = self.main_widget.top_builder_widget.sequence_widget.graph_editor
        GE_blank_pictograph = graph_editor.GE_pictograph_view.blank_pictograph
        if hasattr(GE_blank_pictograph, "grid"):
            GE_blank_pictograph.grid.toggle_non_radial_points_visibility(
                self.non_radial_visible
            )
