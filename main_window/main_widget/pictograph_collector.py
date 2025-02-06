from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographCollector:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def collect_all_pictographs(self) -> List["BasePictograph"]:
        pictographs = []

        sequence_widget = self.main_widget.sequence_widget
        beat_frame = sequence_widget.beat_frame
        beat_views = beat_frame.beat_views
        codex = self.main_widget.learn_tab.codex
        graph_editor = sequence_widget.graph_editor
        option_picker = self.main_widget.construct_tab.option_picker

        pictographs.append(beat_frame.start_pos_view.beat)
        pictographs.extend(beat_view.beat for beat_view in beat_views)

        for pictograph_key_with_scene in self.main_widget.pictograph_cache.values():
            pictographs.extend(
                scene
                for scene in pictograph_key_with_scene.values()
                if scene.view and scene.view.isVisible()
            )

        pictographs.extend(option for option in option_picker.option_pool if option)
        pictographs.append(graph_editor.pictograph_container.GE_view.pictograph)
        codex_views = codex.section_manager.codex_views.values()
        pictographs.extend(view.pictograph for view in codex_views)

        return pictographs
