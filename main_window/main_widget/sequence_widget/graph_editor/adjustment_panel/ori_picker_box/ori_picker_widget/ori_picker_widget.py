from tkinter import END
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QApplication,
)
from PyQt6.QtGui import QIcon, QFont, QFontMetrics, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QPoint, pyqtSignal
from typing import TYPE_CHECKING

from utilities.path_helpers import get_images_and_data_path
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import END_ORI, IN, COUNTER, ORI, OUT, CLOCK, START_ORI
from data.constants import BLUE, RED
from .ori_selection_dialog import OriSelectionDialog

if TYPE_CHECKING:
    from ..ori_picker_box import OriPickerBox


class ClickableLabel(QLabel):
    leftClicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftClicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightClicked.emit()


class OriPickerWidget(QWidget):
    """Widget that displays the 'Orientation' label, current orientation, and controls to adjust it."""

    orientations = [IN, COUNTER, OUT, CLOCK]
    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__()
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color
        self.current_orientation_index = 0

        # References to other components
        self.json_manager = self.ori_picker_box.graph_editor.main_widget.json_manager
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.option_picker = None
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame

        # Setup UI components and layout
        self._setup_components()
        self._setup_layout()
        self._attach_listeners()
        # self._set_initial_orientation()
        # self.resize_ori_picker_widget()

    def _setup_components(self) -> None:
        self.orientation_text = QLabel("Orientation", self)
        self.orientation_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ori_display_label = ClickableLabel(self)
        self.ori_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ori_display_label.setCursor(Qt.CursorShape.PointingHandCursor)

        path = get_images_and_data_path("images/icons")
        self.ccw_button = self._create_rotate_button(
            f"{path}/rotate_ccw.png", self.rotate_ccw
        )
        self.cw_button = self._create_rotate_button(
            f"{path}/rotate_cw.png", self.rotate_cw
        )
        self.rotate_buttons = [self.ccw_button, self.cw_button]

    def _setup_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addStretch(1)
        main_layout.addWidget(self.orientation_text)
        main_layout.addStretch(1)
        main_layout.addWidget(self.ori_display_label)
        main_layout.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ccw_button)
        button_layout.addWidget(self.cw_button)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

    def _attach_listeners(self) -> None:
        self.ori_display_label.leftClicked.connect(self._on_orientation_display_clicked)
        self.ori_display_label.rightClicked.connect(
            self._on_orientation_label_right_clicked
        )
        # self.ccw_button.clicked.connect(self.rotate_ccw)
        # self.cw_button.clicked.connect(self.rotate_cw)
        self.ori_adjusted.connect(self.beat_frame.updater.update_beats_from_json)

    def set_initial_orientation(
        self, start_pos_pictograph: BasePictograph, color: str
    ) -> None:
        if color == "blue":
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "blue_attributes"
            ]["start_ori"]
        else:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "red_attributes"
            ]["start_ori"]
        self.current_orientation_index = self.orientations.index(initial_orientation)
        self.ori_display_label.setText(initial_orientation)

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
        self.ori_display_label.setText(orientation)

        # Update the pictograph and emit orientation changes
        # if the sequence is not empty, then update the start pos
        if len(self.json_manager.loader_saver.load_current_sequence_json()) > 1:
            self.json_manager.start_position_handler.update_start_pos_ori(
                self.color, orientation
            )
            self.json_validation_engine.run(is_current_sequence=True)
            self.ori_adjusted.emit(orientation)

            # Update start position pictograph in the picker if visible
            start_position_pictographs = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.start_pos_picker.pictograph_frame.start_positions
            )
            if start_position_pictographs:
                for pictograph in start_position_pictographs.values():
                    pictograph.props[self.color].updater.update_prop({ORI: orientation})
                    pictograph.updater.update_pictograph()
                    QApplication.processEvents()
            self.option_picker = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.option_picker
            )
            QApplication.processEvents()
            self.option_picker.update_option_picker()
        else:
            # update the start pos picker's pictographs
            start_pos_picker = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.manual_builder.start_pos_picker
            )
            for (
                pictograph
            ) in start_pos_picker.pictograph_frame.start_positions.values():
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )
                pictograph.updater.update_pictograph()
                QApplication.processEvents()

            grid_mode = (
                self.ori_picker_box.graph_editor.sequence_widget.main_widget.settings_manager.global_settings.get_grid_mode()
            )
            if grid_mode == "box":
                pictograph_list = start_pos_picker.start_pos_manager.box_pictographs
            elif grid_mode == "diamond":
                pictograph_list = start_pos_picker.start_pos_manager.diamond_pictographs
            for pictograph in pictograph_list:
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )
                pictograph.updater.update_pictograph()
                QApplication.processEvents()

    def rotate_cw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index + 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self.set_orientation(new_ori)

    def rotate_ccw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index - 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self.set_orientation(new_ori)

    def _create_rotate_button(
        self, icon_path: str, click_function: callable
    ) -> QPushButton:
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(click_function)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def resize_ori_picker_widget(self) -> None:
        self._resize_orientation_label()
        self._resize_ori_display_label()
        self._resize_rotate_buttons()

    def _resize_orientation_label(self) -> None:
        font_size = self.ori_picker_box.graph_editor.width() // 60
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.orientation_text.setFont(font)

    def _resize_ori_display_label(self) -> None:
        font_size = int(self.ori_picker_box.graph_editor.width() // 30)
        font = QFont("Arial", font_size)
        font.setWeight(QFont.Weight.Bold)
        self.ori_display_label.setFont(font)

        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance("counter")
        padding = font_metrics.horizontalAdvance("  ")

        required_width = text_width + padding

        self.ori_display_label.setMinimumWidth(required_width)

        border_size = int(required_width / 60) or 1  # Ensure border size is at least 1
        border_color = self._get_border_color()
        self.ori_display_label.setStyleSheet(
            f"""
            QLabel {{
                border: {border_size}px solid {border_color};
                background-color: white;
            }}
            """
        )

    def _resize_rotate_buttons(self) -> None:
        button_size = int(self.ori_picker_box.graph_editor.height() // 6)
        icon_size = int(button_size * 0.6)
        for button in self.rotate_buttons:
            button.setMinimumSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))

    def _get_border_color(self) -> str:
        if self.color == RED:
            border_color = "#ED1C24"
        elif self.color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"
        return border_color
