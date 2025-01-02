from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .beat_deleter import BeatDeleter


class WidgetCollector:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter

    def collect_widgets(self):
        beats = self.deleter.beat_frame.beats
        pictograph_items = self._get_GE_pictograph_items()
        adjustment_panel_items = self.get_adjustment_panel_items()
        widgets = (
            [
                self.deleter.sequence_widget.current_word_label,
                self.deleter.sequence_widget.difficulty_label,
                self.deleter.beat_frame.start_pos_view,
                self.deleter.beat_frame.selection_overlay,
            ]
            + beats
            + pictograph_items
            + adjustment_panel_items
        )
        return [widget for widget in widgets if widget]

    def _get_GE_pictograph_items(self):
        beat_frame = self.deleter.beat_frame
        GE_pictograph = (
            beat_frame.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )
        arrows = GE_pictograph.arrows.values()
        props = GE_pictograph.props.values()
        tka_glyph_parts = [
            GE_pictograph.tka_glyph.letter_handler.letter_item,
            GE_pictograph.tka_glyph.dash_handler.dash_item,
            GE_pictograph.tka_glyph.dot_handler.same_dot_item,
            GE_pictograph.tka_glyph.dot_handler.opp_dot_item,
        ]
        start_to_end_parts = [
            GE_pictograph.start_to_end_pos_glyph.start_glyph,
            GE_pictograph.start_to_end_pos_glyph.end_glyph,
            GE_pictograph.start_to_end_pos_glyph.arrow_glyph,
        ]
        return list(arrows) + list(props) + tka_glyph_parts + start_to_end_parts

    def get_adjustment_panel_items(self):
        adjustment_panel = self.deleter.sequence_widget.graph_editor.adjustment_panel
        return [
            adjustment_panel.blue_turns_box.turns_widget,
            adjustment_panel.red_turns_box.turns_widget,
            adjustment_panel.blue_turns_box.header,
            adjustment_panel.red_turns_box.header,
            adjustment_panel.blue_ori_picker.header,
            adjustment_panel.red_ori_picker.header,
            adjustment_panel.blue_ori_picker.ori_picker_widget,
            adjustment_panel.red_ori_picker.ori_picker_widget,
        ]
