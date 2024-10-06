from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from main_window.settings_manager.visibility_settings.visibility_settings import VisibilitySettings


class GridVisibilityManager:
    def __init__(self, visibility_settings_handler: "VisibilitySettings") -> None:
        self.visibility_settings_handler = visibility_settings_handler
        self.settings_manager = visibility_settings_handler.settings_manager
        self.non_radial_visible = self.load_nonradial_points_visibility_settings()

    def load_nonradial_points_visibility_settings(self) -> bool:
        return self.visibility_settings_handler.settings["grid_visibility"][
            "non_radial_points"
        ]

    def save_nonradial_points_visibility_settings(self):
        self.visibility_settings_handler.settings["grid_visibility"][
            "non_radial_points"
        ] = self.non_radial_visible
        self.settings_manager.save_settings()

    def set_non_radial_visibility(self, visible: bool):
        self.non_radial_visible = visible
        self.save_nonradial_points_visibility_settings()
        self.apply_visibility_to_all_pictographs()

    def toggle_visibility(self):
        self.non_radial_visible = not self.non_radial_visible
        self.save_nonradial_points_visibility_settings()
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
        ) in sequence_builder.manual_builder.advanced_start_pos_picker.start_pos_cache.items():
            for start_pos in pictograph_list:
                if hasattr(start_pos, "grid"):
                    start_pos.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )

        # apply the change to the GE_BlankPictograph too
        self.main_widget = self.settings_manager.main_window.main_widget
        graph_editor = self.main_widget.top_builder_widget.sequence_widget.graph_editor
        GE_blank_pictograph = (
            graph_editor.pictograph_container.GE_pictograph_view.blank_pictograph
        )
        if hasattr(GE_blank_pictograph, "grid"):
            GE_blank_pictograph.grid.toggle_non_radial_points_visibility(
                self.non_radial_visible
            )
