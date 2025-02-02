from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from base_widgets.base_pictograph.pictograph import Pictograph


class PictographCollector:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def collect_all_pictographs(self) -> List["Pictograph"]:
        return (
            self._collect_from_sequence_workbench()
            + self._collect_from_pictograph_cache()
            + self._collect_from_construct_tab()
            + self._collect_from_graph_editor()
            # + self._collect_from_codex()
        )

    def _collect_from_sequence_workbench(self) -> List["Pictograph"]:
        sequence_workbench = self.main_widget.sequence_workbench
        beat_frame = sequence_workbench.beat_frame
        return [beat_frame.start_pos_view.beat] + [
            beat_view.beat for beat_view in beat_frame.beat_views
        ]

    def _collect_from_pictograph_cache(self) -> List["Pictograph"]:
        return [
            scene
            for pictograph_key_with_scene in self.main_widget.pictograph_cache.values()
            for scene in pictograph_key_with_scene.values()
            if scene.view and scene.view.isVisible()
        ]

    def _collect_from_construct_tab(self) -> List["Pictograph"]:
        construct_tab = self.main_widget.construct_tab
        option_picker = construct_tab.option_picker
        advanced_start_pos_picker = construct_tab.advanced_start_pos_picker
        return (
            [option for option in option_picker.option_pool if option]
            + advanced_start_pos_picker.box_pictographs
            + advanced_start_pos_picker.diamond_pictographs
        )

    def _collect_from_graph_editor(self) -> List["Pictograph"]:
        return [
            self.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_view.pictograph
        ]

    def _collect_from_codex(self) -> List["Pictograph"]:
        return [
            view.pictograph
            for view in self.main_widget.learn_tab.codex.section_manager.codex_views.values()
        ]
