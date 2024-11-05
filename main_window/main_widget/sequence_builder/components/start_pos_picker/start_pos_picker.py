from copy import deepcopy
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from functools import partial
from typing import TYPE_CHECKING
from data.constants import BOX, DIAMOND, START_POS, END_POS
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from ....sequence_widget.beat_frame.start_pos_beat import StartPositionBeat
from .start_pos_picker_variations_button import StartPosVariationsButton
from .start_pos_pictograph_frame import StartPosPickerPictographFrame
from .choose_your_start_pos_label import ChooseYourStartPosLabel
from .base_start_pos_picker import BaseStartPosPicker

if TYPE_CHECKING:
    from ....sequence_builder.manual_builder import ManualBuilderWidget


class StartPosPicker(BaseStartPosPicker):
    SPACING = 10
    start_position_selected = pyqtSignal(BasePictograph)

    def __init__(self, manual_builder: "ManualBuilderWidget"):
        super().__init__(manual_builder)
        self.top_builder_widget = None
        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.button_layout = self._setup_variations_button_layout()
        self.setup_layout()
        self.setObjectName("StartPosPicker")
        self.setStyleSheet("background-color: white;")
        self.initialized = False
        self.start_options: dict[str, BasePictograph] = {}

        self.start_position_selected.connect(
            self.manual_builder.transition_to_sequence_building
        )
        self.display_variations(
            self.main_widget.settings_manager.global_settings.get_grid_mode()
        )

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.start_label_layout = QHBoxLayout()
        self.pictograph_layout = QHBoxLayout()

        self.start_label_layout.addWidget(self.choose_your_start_pos_label)
        self.pictograph_layout.addWidget(self.pictograph_frame)

        self.layout.addStretch(1)
        self.layout.addLayout(self.start_label_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_layout)
        self.layout.addStretch(1)

    def _setup_variations_button_layout(self) -> QHBoxLayout:
        self.variations_button = StartPosVariationsButton(self)
        self.variations_button.clicked.connect(
            self.manual_builder.transition_to_advanced_start_pos_picker
        )
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.variations_button)
        button_layout.addStretch(1)
        return button_layout

    def display_variations(self, grid_mode: str) -> None:
        """Load only the start positions relevant to the current grid mode."""
        # clear all previous start options
        self.pictograph_frame.clear_pictographs()

        start_pos_keys = (
            ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
            if grid_mode == DIAMOND
            else ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
        )
        if grid_mode == BOX:
            self.get_box_variations()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(position_key, BOX)
        elif grid_mode == DIAMOND:
            self.get_diamond_variations()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(
                    position_key, DIAMOND
                )

    def _add_start_position_option_to_start_pos_frame(
        self, position_key: str, grid_mode: str
    ) -> None:
        """Adds an option for the specified start position based on the current grid mode."""
        start_pos, end_pos = position_key.split("_")
        for letter, pictograph_dicts in self.main_widget.pictograph_dicts.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    # Use the cached pictograph if available
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_dict, grid_mode
                    )
                    self.start_options[letter] = pictograph
                    pictograph.letter = letter
                    pictograph.start_pos = start_pos
                    pictograph.end_pos = end_pos
                    self.pictograph_frame._add_start_pos_to_layout(pictograph)
                    pictograph.view.mousePressEvent = partial(
                        self.add_start_pos_to_sequence,
                        pictograph,
                    )
                    pictograph.start_to_end_pos_glyph.hide()
                    break  # Assuming only one pictograph per position_key

    def add_start_pos_to_sequence(
        self, clicked_start_option: BasePictograph, event: QWidget = None
    ) -> None:
        """Handle the start position click event."""
        sequence_widget = self.main_widget.sequence_widget
        start_position_beat = StartPositionBeat(sequence_widget.beat_frame)
        clicked_start_option.updater.update_dict_from_attributes()
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )

        sequence_widget.beat_frame.start_pos_view.set_start_pos(start_position_beat)
        self.manual_builder.last_beat = start_position_beat
        beat_frame = sequence_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_overlay.select_beat(start_pos_view)

        self.main_widget.json_manager.start_position_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def resize_start_pos_picker(self) -> None:
        spacing = 10
        for start_option in self.start_options.values():
            view_width = int((self.width() // 5) - spacing)
            start_option.view.setFixedSize(view_width, view_width)
            start_option.view.view_scale = view_width / start_option.width()
            start_option.view.resetTransform()
            start_option.view.scale(
                start_option.view.view_scale, start_option.view.view_scale
            )
            start_option.container.styled_border_overlay.resize_styled_border_overlay()
        self.pictograph_frame.resize_start_pos_picker_pictograph_frame()
        self.variations_button.resize_variations_button()
