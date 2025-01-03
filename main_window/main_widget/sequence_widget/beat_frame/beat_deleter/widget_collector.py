from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .beat_deleter import BeatDeleter


class WidgetCollector:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter

    def collect_shared_widgets(self):
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
        GE_pictograph = (
            self.deleter.beat_frame.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )

        items = []
        items.extend(GE_pictograph.arrows.values())
        items.extend(GE_pictograph.props.values())

        glyph_items = [
            GE_pictograph.tka_glyph.letter_item,
            GE_pictograph.tka_glyph.dash_handler.dash_item,
            GE_pictograph.tka_glyph.dot_handler.same_dot_item,
            GE_pictograph.tka_glyph.dot_handler.opp_dot_item,
            GE_pictograph.start_to_end_pos_glyph.start_glyph,
            GE_pictograph.start_to_end_pos_glyph.end_glyph,
            GE_pictograph.start_to_end_pos_glyph.arrow_glyph,
            GE_pictograph.elemental_glyph,
            GE_pictograph.vtg_glyph,
            GE_pictograph.number_item,
            GE_pictograph.blue_reversal_symbol,
            GE_pictograph.red_reversal_symbol,
            GE_pictograph.start_text_item,
            GE_pictograph.tka_glyph.turns_column_handler.top_number_item,
            GE_pictograph.tka_glyph.turns_column_handler.bottom_number_item,
        ]

        items.extend(glyph_items)

        return items

    def get_adjustment_panel_items(self):
        panel = self.deleter.sequence_widget.graph_editor.adjustment_panel
        items = []
        turns_boxes = [panel.blue_turns_box, panel.red_turns_box]
        ori_pickers = [panel.blue_ori_picker, panel.red_ori_picker]

        for turns_box in turns_boxes:
            items.extend(
                [
                    turns_box.turns_widget.turns_display_frame.turns_label,
                    turns_box.turns_widget.motion_type_label,
                    turns_box.prop_rot_dir_button_manager.ccw_button,
                    turns_box.prop_rot_dir_button_manager.cw_button,
                ]
            )
        for ori_picker in ori_pickers:
            items.extend([ori_picker.ori_picker_widget])

        return items
