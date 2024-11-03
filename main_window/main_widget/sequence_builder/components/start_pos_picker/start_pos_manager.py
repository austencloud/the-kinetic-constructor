from copy import deepcopy
from functools import partial
from PyQt6.QtCore import QObject, pyqtSignal
from Enums.letters import Letter
from data.constants import BOX, DIAMOND, END_POS, START_POS
from ....sequence_widget.beat_frame.start_pos_beat import StartPositionBeat
from base_widgets.base_pictograph.base_pictograph import BasePictograph


from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    start_position_selected = pyqtSignal(BasePictograph)

    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__()
        self.manual_builder = start_pos_picker.manual_builder
        self.start_pos_picker = start_pos_picker
        self.start_pos_frame = start_pos_picker.pictograph_frame
        self.main_widget = start_pos_picker.manual_builder.main_widget
        self.top_builder_widget = None
        self.start_options: dict[str, BasePictograph] = {}
        self.setup_start_positions()
        self.start_position_selected.connect(
            self.manual_builder.transition_to_sequence_building
        )

    def clear_start_positions(self) -> None:
        """Clears the start positions."""
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def setup_start_positions(self) -> None:
        """Setup initial orientations and show options for the starting position."""
        grid_mode = self.main_widget.settings_manager.global_settings.get_grid_mode()
        start_pos_keys = (
            ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
            if grid_mode == DIAMOND
            else ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
        )

        for position_key in start_pos_keys:
            self._add_start_position_option_to_start_pos_frame(position_key)

        # Set initial orientation in the OriPickerBox to "IN" if no orientation specified
        if self.start_options:
            initial_pictograph = next(iter(self.start_options.values()))
            blue_orientation = initial_pictograph.pictograph_dict[
                "blue_attributes"
            ].get("start_ori", "IN")
            red_orientation = initial_pictograph.pictograph_dict["red_attributes"].get(
                "start_ori", "IN"
            )

            # Update OriPickerBox for blue and red orientations
            self.graph_editor = (
                self.start_pos_frame.start_pos_picker.main_widget.sequence_widget.graph_editor
            )
            # self.graph_editor.adjustment_panel.blue_ori_picker.set_initial_orientation(blue_orientation)
            # self.graph_editor.adjustment_panel.red_ori_picker.set_initial_orientation(red_orientation)

    def _add_start_position_option_to_start_pos_frame(self, position_key: str) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for (
            letter,
            pictograph_dicts,
        ) in self.manual_builder.main_widget.pictograph_dicts.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_position_pictograph = BasePictograph(
                        self.start_pos_picker.main_widget,
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
                        self.add_start_pos_to_sequence,
                        start_position_pictograph,
                    )
                    start_position_pictograph.start_to_end_pos_glyph.hide()

    def add_start_pos_to_sequence(
        self, clicked_start_option: BasePictograph, event: QWidget = None
    ) -> None:
        """Handle the start position click event."""
        self.sequence_widget = self.main_widget.sequence_widget
        start_position_beat = StartPositionBeat(
            self.main_widget.sequence_widget.beat_frame,
        )
        clicked_start_option.updater.update_dict_from_attributes()
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )

        self.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_position_beat
        )
        self.manual_builder.last_beat = start_position_beat
        beat_frame = self.sequence_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_overlay.select_beat(start_pos_view)

        self.main_widget.json_manager.start_position_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def hide_start_positions(self) -> None:
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget.sequence_widget.beat_frame,
        )
        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_dict
        )

        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "BasePictograph":
        if not start_pos_data:
            return None
        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.pictograph_dicts.get(letter, [])
        for pictograph_dict in matching_letter_pictographs:
            if pictograph_dict["start_pos"] == start_pos_key:

                pictograph_dict["blue_attributes"]["start_ori"] = start_pos_data[
                    "blue_attributes"
                ]["end_ori"]
                pictograph_dict["red_attributes"]["start_ori"] = start_pos_data[
                    "red_attributes"
                ]["end_ori"]
                pictograph_factory = (
                    self.main_widget.sequence_widget.beat_frame.beat_factory
                )
                pictograph_key = (
                    self.main_widget.pictograph_key_generator.generate_pictograph_key(
                        pictograph_dict
                    )
                )
                start_pos_pictograph = pictograph_factory.create_start_pos_beat(
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

    def get_all_start_positions(self) -> list["BasePictograph"]:
        all_start_positions = []
        valid_letters = [Letter.α, Letter.β, Letter.Γ]
        for letter in self.main_widget.pictograph_dicts:
            if letter in valid_letters:
                all_start_positions.extend(self.get_variations(letter))
        return all_start_positions

    def get_variations(self, start_pos_letter: str) -> list[BasePictograph]:
        variations = []
        for pictograph_dict in self.main_widget.pictograph_dicts[start_pos_letter]:
            if (
                self.main_widget.settings_manager.global_settings.get_grid_mode()
                == DIAMOND
            ):
                if pictograph_dict["start_pos"] not in [
                    "alpha1",
                    "alpha3",
                    "alpha5",
                    "alpha7",
                    "beta1",
                    "beta3",
                    "beta5",
                    "beta7",
                    "gamma1",
                    "gamma3",
                    "gamma5",
                    "gamma7",
                    "gamma9",
                    "gamma11",
                    "gamma13",
                    "gamma15",
                ]:
                    continue
                pictograph = self.create_pictograph_from_dict(pictograph_dict)
            elif (
                self.main_widget.settings_manager.global_settings.get_grid_mode() == BOX
            ):
                if pictograph_dict["start_pos"] not in [
                    "alpha2",
                    "alpha4",
                    "alpha6",
                    "alpha8",
                    "beta2",
                    "beta4",
                    "beta6",
                    "beta8",
                    "gamma2",
                    "gamma4",
                    "gamma6",
                    "gamma8",
                    "gamma10",
                    "gamma12",
                    "gamma14",
                    "gamma16",
                ]:
                    continue
                pictograph = self.create_pictograph_from_dict(pictograph_dict)
            variations.append(pictograph)
        return variations

    def create_pictograph_from_dict(self, pictograph_dict: dict) -> BasePictograph:
        pictograph = BasePictograph(self.main_widget)
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph

    def resize_start_position_pictographs(self) -> None:
        spacing = 10
        for start_option in self.start_options.values():
            view_width = int(
                (self.start_pos_frame.start_pos_picker.main_widget.width() // 8)
                - spacing
            )
            start_option.view.setFixedSize(view_width, view_width)
            start_option.view.view_scale = view_width / start_option.width()
            start_option.view.resetTransform()
            start_option.view.scale(
                start_option.view.view_scale, start_option.view.view_scale
            )
            start_option.container.styled_border_overlay.resize_styled_border_overlay()
