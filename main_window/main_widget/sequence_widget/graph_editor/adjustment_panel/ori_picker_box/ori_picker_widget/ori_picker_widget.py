# ori_picker_widget.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QSize, QPoint, pyqtSignal
from typing import TYPE_CHECKING
from data.constants import (
    HEX_BLUE,
    HEX_RED,
    IN,
    COUNTER,
    OUT,
    CLOCK,
    START_ORI,
    END_ORI,
    RED,
    BLUE,
    BOX,
    DIAMOND,
)
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.clickable_ori_label import (
    ClickableOriLabel,
)
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_text_label import (
    OrientationTextLabel,
)
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.rotate_button import (
    RotateButton,
)
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.rotate_buttons_widget import (
    RotateButtonsWidget,
)
from utilities.path_helpers import get_images_and_data_path
from copy import deepcopy

# Assuming the ClickableOriLabel and OriSelectionDialog are needed
from .ori_selection_dialog import OriSelectionDialog

if TYPE_CHECKING:
    from ..ori_picker_box import OriPickerBox
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OriPickerWidget(QWidget):
    """Minimalist widget that displays the orientation controls."""

    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color
        self.current_orientation_index = 0
        self.orientations = [IN, COUNTER, OUT, CLOCK]

        self.json_manager = self.ori_picker_box.graph_editor.main_widget.json_manager
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.option_picker = None
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame

        # Instantiate components
        self.orientation_label = OrientationTextLabel(self)
        self.clickable_ori_label = ClickableOriLabel(self)
        self.rotate_buttons_widget = RotateButtonsWidget(self)

        # Setup layout
        self._setup_layout()

        # Attach listeners
        self._attach_listeners()

    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addStretch(1)
        main_layout.addWidget(self.orientation_label)
        main_layout.addStretch(1)
        main_layout.addWidget(self.clickable_ori_label)
        main_layout.addStretch(1)

        # Rotate buttons layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.rotate_buttons_widget)

        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

    def _attach_listeners(self):
        self.clickable_ori_label.leftClicked.connect(
            self._on_orientation_display_clicked
        )
        self.clickable_ori_label.rightClicked.connect(
            self._on_orientation_label_right_clicked
        )
        self.ori_adjusted.connect(self.beat_frame.updater.update_beats_from_json)

    def set_initial_orientation(
        self, start_pos_pictograph: "BasePictograph", color: str
    ) -> None:
        if color == BLUE:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "blue_attributes"
            ][START_ORI]
        else:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "red_attributes"
            ][START_ORI]
        self.current_orientation_index = self.orientations.index(initial_orientation)
        self.clickable_ori_label.setText(initial_orientation)

    def _on_orientation_display_clicked(self):
        dialog = OriSelectionDialog(self)
        dialog.move(self.mapToGlobal(QPoint(0, 0)))
        if dialog.exec():
            new_orientation = dialog.selected_orientation
            self.set_orientation(new_orientation)

    def _on_orientation_label_right_clicked(self):
        current_ori = self.orientations[self.current_orientation_index]
        if current_ori in [IN, OUT]:
            new_ori = OUT if current_ori == IN else IN
        elif current_ori in [CLOCK, COUNTER]:
            new_ori = COUNTER if current_ori == CLOCK else CLOCK
        else:
            new_ori = current_ori
        self.set_orientation(new_ori)

    def set_orientation(self, orientation: str) -> None:
        """Set the displayed orientation and apply it to the related pictograph."""
        self.current_orientation_index = self.orientations.index(orientation)
        self.clickable_ori_label.setText(orientation)

        if len(self.json_manager.loader_saver.load_current_sequence_json()) > 1:
            self.json_manager.start_position_handler.update_start_pos_ori(
                self.color, orientation
            )
            self.json_validation_engine.run(is_current_sequence=True)
            self.ori_adjusted.emit(orientation)

            start_position_pictographs = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.start_pos_picker.pictograph_frame.start_positions
            )
            if start_position_pictographs:
                for pictograph in start_position_pictographs.values():
                    pictograph.updater.update_pictograph(
                        {
                            f"{self.color}_attributes": {
                                START_ORI: orientation,
                                END_ORI: orientation,
                            }
                        }
                    )
            self.option_picker = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.option_picker
            )
            self.option_picker.update_option_picker()
        else:
            start_pos_picker = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.start_pos_picker
            )
            advanced_start_pos_picker = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.advanced_start_pos_picker
            )
            for pictograph in start_pos_picker.start_options.values():
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

            grid_mode = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.settings_manager.global_settings.get_grid_mode()
            )
            if grid_mode == BOX:
                pictograph_list = advanced_start_pos_picker.box_pictographs
            elif grid_mode == DIAMOND:
                pictograph_list = advanced_start_pos_picker.diamond_pictographs
            else:
                pictograph_list = []
            for pictograph in pictograph_list:
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

    def resize_ori_picker_widget(self) -> None:
        self.orientation_label.resize_orientation_label()
        self.clickable_ori_label.resize_clickable_ori_label()
        self.rotate_buttons_widget.resize_rotate_buttons_widget()

    def _get_border_color(self) -> str:
        if self.color == RED:
            return HEX_RED
        elif self.color == BLUE:
            return HEX_BLUE
        else:
            return "black"
