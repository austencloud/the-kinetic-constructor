from copy import deepcopy
from functools import partial
from PyQt6.QtCore import QObject, pyqtSignal
from Enums.letters import Letter
from data.constants import END_POS, START_POS
from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat
from widgets.pictograph.pictograph import Pictograph

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__()
        self.sequence_builder = start_pos_picker.sequence_builder
        self.start_pos_picker = start_pos_picker
        self.start_pos_frame = start_pos_picker.pictograph_frame
        self.main_widget = start_pos_picker.sequence_builder.main_widget
        self.top_builder_widget = self.sequence_builder.top_builder_widget
        self.start_options: dict[str, Pictograph] = {}
        self.setup_start_positions()
        self.start_position_selected.connect(
            self.sequence_builder.transition_to_sequence_building
        )

    def setup_start_positions(self) -> None:
        """Shows options for the starting position."""
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_position(position_key)

    def _add_start_position(self, position_key: str) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for (
            letter,
            pictograph_dicts,
        ) in self.sequence_builder.main_widget.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_position_pictograph = (
                        self.start_pos_picker.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_position_pictograph
                    start_position_pictograph.letter = letter
                    start_position_pictograph.start_pos = start_pos
                    start_position_pictograph.end_pos = end_pos
                    self.start_pos_frame._add_start_pos_to_layout(
                        start_position_pictograph
                    )
                    start_position_pictograph.updater.update_pictograph(pictograph_dict)

                    start_position_pictograph.view.mousePressEvent = partial(
                        self.on_start_pos_clicked, start_position_pictograph
                    )
                    start_position_pictograph.start_to_end_pos_glyph.hide()

    def on_start_pos_clicked(
        self, clicked_start_option: Pictograph, event: QWidget = None
    ) -> None:
        """Handle the start position click event."""
        start_position_beat = StartPositionBeat(
            self.top_builder_widget.sequence_widget.beat_frame,
        )
        clicked_start_option.updater.update_dict_from_attributes()
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )

        self.sequence_builder.top_builder_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_position_beat
        )
        self.sequence_builder.last_beat = start_position_beat
        beat_frame = self.sequence_builder.top_builder_widget.sequence_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_overlay.select_beat(start_pos_view)

        self.main_widget.json_manager.start_position_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def hide_start_positions(self) -> None:
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def resize_start_position_pictographs(self) -> None:
        spacing = 10
        for start_option in self.start_options.values():
            view_width = int((self.start_pos_frame.width() // 4) - spacing)
            start_option.view.setFixedSize(view_width, view_width)
            start_option.view.view_scale = view_width / start_option.width()
            start_option.view.resetTransform()
            start_option.view.scale(
                start_option.view.view_scale, start_option.view.view_scale
            )
            start_option.container.styled_border_overlay.resize_styled_border_overlay()

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget.top_builder_widget.sequence_widget.beat_frame,
        )
        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_dict
        )

        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "Pictograph":
        if not start_pos_data:
            return None
        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.letters.get(letter, [])
        for pictograph_dict in matching_letter_pictographs:
            if pictograph_dict["start_pos"] == start_pos_key:

                pictograph_dict["blue_attributes"]["start_ori"] = start_pos_data[
                    "blue_attributes"
                ]["end_ori"]
                pictograph_dict["red_attributes"]["start_ori"] = start_pos_data[
                    "red_attributes"
                ]["end_ori"]
                pictograph_factory = (
                    self.main_widget.top_builder_widget.sequence_widget.pictograph_factory
                )
                pictograph_key = (
                    self.main_widget.pictograph_key_generator.generate_pictograph_key(
                        pictograph_dict
                    )
                )
                start_pos_pictograph = pictograph_factory.get_or_create_pictograph(
                    pictograph_key, pictograph_dict
                )
                return start_pos_pictograph

        print(f"No matching start position found for key: {start_pos_key}")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str) -> str:
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None

    def get_all_start_positions(self) -> list["Pictograph"]:
        all_start_positions = []
        valid_letters = [Letter.α, Letter.β, Letter.Γ]
        for letter in self.main_widget.letters:
            if letter in valid_letters:
                all_start_positions.extend(self.get_variations(letter))
        return all_start_positions

    def get_variations(self, start_pos_letter: str) -> list[Pictograph]:
        variations = []
        for pictograph_dict in self.main_widget.letters[start_pos_letter]:
            pictograph = self.create_pictograph_from_dict(pictograph_dict)
            variations.append(pictograph)
        return variations

    def create_pictograph_from_dict(self, pictograph_dict: dict) -> Pictograph:
        pictograph = Pictograph(self.main_widget)
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph
