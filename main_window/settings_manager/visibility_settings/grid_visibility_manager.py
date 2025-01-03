from typing import TYPE_CHECKING

from base_widgets.base_pictograph.base_pictograph import BasePictograph

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
        self.apply_grid_visibility()

    def set_non_radial_visibility(self, visible: bool):
        self.non_radial_visible = visible
        self.save_non_radial_visibility(visible)

    def toggle_visibility(self):
        self.non_radial_visible = not self.non_radial_visible
        # self.save_non_radial_visibility(self.non_radial_visible)

    def apply_grid_visibility(self):
        def toggle_visibility(obj: "BasePictograph"):
            obj.grid.toggle_non_radial_points_visibility(self.non_radial_visible)

        main_widget = self.settings_manager.main_window.main_widget

        # Collections to apply visibility
        beat_views = main_widget.sequence_widget.beat_frame.beats
        beats = []
        # create a list of beat_view.beat for each beat_view
        for view in beat_views:
            beats.extend([view.beat])
        collections = [
            [main_widget.construct_tab.option_picker.option_pool],
            [
                (
                    [main_widget.sequence_widget.beat_frame.start_pos_view.beat]
                    if main_widget.sequence_widget.beat_frame.start_pos_view.isVisible()
                    else []
                )
            ],
            beats,
            list(
                main_widget.construct_tab.advanced_start_pos_picker.start_pos_cache.values()
            ),
            [
                [
                    main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view.pictograph
                ]
            ],
        ]

        # recursively remove all empty lists and dicts from the collections
        def clean_collections(collections):
            cleaned = []
            for item in collections:
                if isinstance(item, list):
                    cleaned_item = clean_collections(item)
                    if cleaned_item:
                        cleaned.append(cleaned_item)
                elif isinstance(item, dict):
                    if item:
                        cleaned.append(item)
                else:
                    cleaned.append(item)
            return cleaned

        collections = clean_collections(collections)

        # get all the pictographs from the lists within the collection, put everything in one list
        def extract_pictographs(collection):
            pictographs = []
            if isinstance(collection, list):
                for item in collection:
                    if isinstance(item, list):
                        for pictograph in extract_pictographs(item):
                            pictographs.append(pictograph)
                    else:
                        pictographs.extend(extract_pictographs(item))
            elif isinstance(collection, dict):
                for item in collection.values():
                    pictographs.extend(extract_pictographs(item))
            else:
                pictographs.append(collection)
            return pictographs

        pictographs = extract_pictographs(collections)

        for pictograph in pictographs:
            toggle_visibility(pictograph)
