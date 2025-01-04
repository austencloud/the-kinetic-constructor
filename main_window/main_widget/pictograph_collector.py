from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographCollector:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def collect_all_pictographs(self) -> List["BasePictograph"]:
        pictographs = []

        # Collect pictographs from beat views
        beat_views = self.main_widget.sequence_widget.beat_frame.beats
        pictographs.extend(beat_view.beat for beat_view in beat_views)

        # Collect pictographs from pictograph cache
        for pictograph_key_with_scene in self.main_widget.pictograph_cache.values():
            pictographs.extend(
                scene for scene in pictograph_key_with_scene.values()
                if scene.view and scene.view.isVisible()
            )

        # Collect pictographs from option picker
        pictographs.extend(
            option for option in self.main_widget.construct_tab.option_picker.option_pool
            if option
        )

        # Collect start position beat
        pictographs.append(
            self.main_widget.sequence_widget.beat_frame.start_pos_view.beat
        )

        # Collect graph editor pictograph
        pictographs.append(
            self.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )

        # Collect codex pictographs
        codex_views = self.main_widget.learn_tab.codex.section_manager.codex_views.values()
        pictographs.extend(view.pictograph for view in codex_views)

        return pictographs
