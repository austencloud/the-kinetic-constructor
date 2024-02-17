import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.indicator_label import IndicatorLabel
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.sequence_widget_pictograph_factory import (
    SequenceWidgetPictographFactory,
)
from widgets.sequence_widget.beat_frame.beat import Beat
from widgets.sequence_widget.beat_frame.beat_frame import SequenceBeatFrame
from widgets.sequence_widget.beat_frame.beat_selection_overlay import (
    BeatSelectionOverlay,
)
from widgets.sequence_widget.button_frame import SequenceButtonFrame
from widgets.sequence_widget.sequence_modifier_tab_widget import (
    SequenceModifierTabWidget,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.pictograph_cache: dict[str, Pictograph] = {}
        self.indicator_label = IndicatorLabel(self)
        self.beat_selection_overlay = BeatSelectionOverlay(self)
        self.beat_frame = SequenceBeatFrame(self.main_widget, self)
        self.button_frame = SequenceButtonFrame(self)
        self.pictograph_factory = SequenceWidgetPictographFactory(
            self, self.pictograph_cache
        )
        self.sequence_modifier_tab_widget = SequenceModifierTabWidget(self)
        self.beats = self.beat_frame.beats
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.beat_frame, 8)
        self.layout.addWidget(self.button_frame, 1)
        self.layout.addWidget(self.indicator_label, 1)
        self.layout.addWidget(self.sequence_modifier_tab_widget, 3)

    def save_sequence(sequence: list[Pictograph], filename: str) -> None:
        sequence_data = [pictograph.get.pictograph_dict() for pictograph in sequence]
        with open(filename, "w") as file:
            json.dump(sequence_data, file, indent=4)

    def populate_sequence(self, pictograph_dict: dict) -> None:
        pictograph = Beat(self.main_widget)
        pictograph.updater.update_pictograph(pictograph_dict)
        self.beat_frame.add_scene_to_sequence(pictograph)
        pictograph_key = (
            pictograph.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_dict
            )
        )
        self.pictograph_cache[pictograph_key] = pictograph

    def resize_sequence_widget(self) -> None:
        self.setMinimumWidth(int(self.main_widget.width() * 3 / 8))
        beat_view_width = int(self.width() / self.beat_frame.COLUMN_COUNT)
        for beat_view in self.beat_frame.beats:
            beat_view.setMaximumWidth(beat_view_width)
            beat_view.setMaximumHeight(beat_view_width)
            beat_view.view_scale = beat_view_width / beat_view.beat.width()
            beat_view.resetTransform()
            beat_view.scale(beat_view.view_scale, beat_view.view_scale)
            beat_view.beat.container.styled_border_overlay.resize_styled_border_overlay()
        self.beat_frame.start_pos_view.setMaximumWidth(beat_view_width)
        self.beat_frame.start_pos_view.setMaximumHeight(beat_view_width)
        self.sequence_modifier_tab_widget.resize_sequence_modifier_tab_widget()
        self.layout.update()



    # TODO: Implement the following methods

    # def delete_selected_pictograph(self):
    #     # This method assumes you have a way to track the currently selected pictograph.
    #     # Let's assume selected_beat is the variable holding the currently selected BeatView.
    #     selected_index = self.beats.index(self.selected_beat)
    #     for beat_view in self.beats[selected_index:]:
    #         beat_view.clear()  # You might need to implement this method to clear the beat view.
    #     self.update_option_picker()

    # def update_option_picker(self):
    #     # This method will refresh the option picker to reflect the current state of the sequence.
    #     # Assuming you have a method in OptionPicker that updates its state.
    #     last_filled_beat = self.beat_frame.get_last_beat()
    #     self.main_widget.option_picker.update_based_on_last_beat(last_filled_beat)
