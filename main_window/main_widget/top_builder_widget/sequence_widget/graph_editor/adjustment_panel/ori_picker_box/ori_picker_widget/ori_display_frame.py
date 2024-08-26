from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, QSize, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from typing import TYPE_CHECKING
from utilities.path_helpers import get_images_and_data_path
from widgets.base_widgets.pictograph.base_pictograph import BasePictograph

from data.constants import IN, COUNTER, ORI, OUT, CLOCK
from data.constants import BLUE, RED
from .ori_selection_dialog import OriSelectionDialog

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OriDisplayFrame(QFrame):
    """Contains the orientation display label and the buttons to adjust the orientation."""

    orientations = [IN, COUNTER, OUT, CLOCK]
    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_widget: "OriPickerWidget") -> None:
        super().__init__(ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        self.ori_picker_box = self.ori_picker_widget.ori_picker_box
        self.json_manager = self.ori_picker_box.graph_editor.main_widget.json_manager
        self.json_validation_engine = (
            self.ori_picker_box.graph_editor.main_widget.json_manager.validation_engine
        )
        self.option_picker = (
            self.ori_picker_box.graph_editor.sequence_widget.top_builder_widget.sequence_builder.option_picker
        )
        self.color = self.ori_picker_box.color
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame
        self._setup_components()
        self._setup_layout()
        self._attach_listeners()
        self._setup_current_orientation_display()

    def _setup_current_orientation_display(self) -> None:
        self.ori_display_label = self.ori_display_label
        self.ori_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ori_display_label.mousePressEvent = self._on_orientation_display_clicked

    def _get_border_color(self) -> str:
        if self.ori_picker_box.color == RED:
            border_color = "#ED1C24"
        elif self.ori_picker_box.color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"
        return border_color

    def _setup_components(self) -> None:
        self._setup_rotate_buttons()
        self._setup_ori_display_label()

    def _setup_ori_display_label(self):
        self.ori_display_label = QLabel(self)
        self.ori_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_rotate_buttons(self):
        path = get_images_and_data_path("images/icons")
        self.ccw_button = self._setup_rotate_button(
            f"{path}/rotate_ccw.png", self.rotate_ccw
        )
        self.cw_button = self._setup_rotate_button(
            f"{path}/rotate_cw.png", self.rotate_cw
        )
        self.rotate_buttons = [self.ccw_button, self.cw_button]

    def _on_orientation_display_clicked(self, event) -> None:
        dialog = OriSelectionDialog(self)
        dialog.move(self.mapToGlobal(QPoint(0, 0)))
        if dialog.exec():
            new_orientation = dialog.selected_orientation
            self.set_orientation(new_orientation)

    def set_orientation(self, orientation):
        self.current_orientation_index = self.orientations.index(orientation)
        self.ori_display_label.setText(orientation)
        self.json_manager.start_position_handler.update_start_pos_ori(
            self.color, orientation
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.ori_adjusted.emit(orientation)
        current_pictograph = (
            self.ori_picker_box.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )
        current_pictograph.props[self.color].updater.update_prop({ORI: orientation})
        current_pictograph.updater.update_pictograph()
        QApplication.processEvents()
        self.option_picker.update_option_picker()

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ccw_button)
        button_layout.addWidget(self.cw_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ori_display_label)
        layout.addLayout(button_layout)

    def _attach_listeners(self) -> None:
        self.ori_display_label.mousePressEvent = self._on_orientation_display_clicked
        self.ori_adjusted.connect(self.beat_frame.on_beat_adjusted)

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

    def _setup_rotate_button(
        self, icon_path: str, click_function: callable
    ) -> QPushButton:
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(click_function)
        button.setFixedSize(40, 40)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

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

    def resize_ori_display_frame(self) -> None:
        self._resize_ori_label()
        self._resize_ori_buttons()

    def _resize_ori_label(self) -> None:
        ori_label_width = int(self.ori_picker_box.width() // 1.5)
        ori_label_height = self.ori_picker_box.height() // 4
        self.ori_display_label.setFixedSize(ori_label_width, ori_label_height)
        border_size = int(self.ori_display_label.width() / 60)
        border_color = self._get_border_color()
        font_size = int(self.ori_picker_box.graph_editor.width() // 30)
        font = QFont("Arial", font_size)
        font.setWeight(QFont.Weight.Bold)
        self.ori_display_label.setFont(font)
        self.ori_display_label.setStyleSheet(
            f"""
            QLabel {{
                border: {border_size}px solid {border_color};
                background-color: white;

            }}
            """
        )

    def _resize_ori_buttons(self) -> None:
        button_size = int(self.ori_picker_box.height() // 4)
        icon_size = int(button_size * 0.6)
        for button in self.rotate_buttons:
            button.setFixedSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))
