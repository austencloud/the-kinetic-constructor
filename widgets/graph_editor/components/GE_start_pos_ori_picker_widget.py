from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)
from PyQt6.QtGui import QIcon, QFont

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from constants import IN, ORI, OUT, CLOCK, COUNTER
from typing import TYPE_CHECKING

from path_helpers import get_images_and_data_path
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker_box import (
        GE_StartPosOriPickerBox,
    )


class GE_StartPosOriPickerWidget(QWidget):
    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "GE_StartPosOriPickerBox") -> None:
        super().__init__()
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color
        self.json_validation_engine = (
            self.ori_picker_box.graph_editor.main_widget.json_manager.current_sequence_json_handler.validation_engine
        )
        self.beat_frame = (
            self.ori_picker_box.graph_editor.sequence_modifier.sequence_widget.beat_frame
        )
        self.current_sequence_json_handler = (
            self.ori_picker_box.graph_editor.main_widget.json_manager.current_sequence_json_handler
        )
        self.option_picker = (
            self.ori_picker_box.graph_editor.main_widget.main_builder_widget.sequence_builder.option_picker
        )
        self.current_orientation_index = 0
        self.orientations = [IN, COUNTER, OUT, CLOCK]
        self._setup_orientation_label()
        self._setup_orientation_control_layout()
        self._setup_layout()
        self.ori_adjusted.connect(self.beat_frame.on_beat_adjusted)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.layout.addWidget(self.ori_label, 1)
        self.layout.addWidget(self.current_orientation_display, 1)
        self.layout.addStretch(3)
        self.layout.addLayout(self.orientation_control_layout, 1)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def _setup_orientation_label(self) -> None:
        self.ori_label = QLabel("Orientation")
        self.ori_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _set_ori_label_font_size(self) -> None:
        ori_label_font_size = self.ori_picker_box.graph_editor.width() // 50
        font = QFont("Cambria", ori_label_font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.ori_label.setFont(font)

    def _setup_orientation_control_layout(self) -> None:
        path = get_images_and_data_path("images/icons")
        self.ccw_button = self.setup_button(f"{path}/rotate_ccw.png", self.rotate_ccw)
        self.current_orientation_display = self.setup_current_orientation_display()
        self.cw_button = self.setup_button(f"{path}/rotate_cw.png", self.rotate_cw)
        self.orientation_control_layout = QHBoxLayout()
        self.orientation_control_layout.addStretch(5)
        self.orientation_control_layout.addWidget(self.ccw_button)
        self.orientation_control_layout.addStretch(3)
        self.orientation_control_layout.addWidget(self.cw_button)
        self.orientation_control_layout.addStretch(5)

    def setup_button(self, icon_path, click_function: callable) -> QPushButton:
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(click_function)
        button.setFixedSize(40, 40)
        return button

    def setup_current_orientation_display(self) -> QLabel:
        self.current_orientation_display = QLabel(
            self.orientations[self.current_orientation_index]
        )
        self.current_orientation_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self.current_orientation_display

    def set_current_orientation_display_font(self) -> None:
        font = QFont("Cambria")
        font_size = self.ori_picker_box.graph_editor.width() // 25
        font.setPointSize(font_size)
        font.setWeight(QFont.Weight.Bold)
        self.current_orientation_display.setFont(font)

    def rotate_cw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index + 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self.current_orientation_display.setText(new_ori)
        current_pictograph = (
            self.ori_picker_box.graph_editor.GE_pictograph_view.pictograph
        )
        self.current_sequence_json_handler.update_start_pos_ori(self.color, new_ori)
        self.json_validation_engine.run()
        self.ori_adjusted.emit(new_ori)
        current_pictograph.props[self.color].updater.update_prop({ORI: new_ori})
        current_pictograph.updater.update_pictograph()
        QApplication.processEvents()
        self.option_picker.update_option_picker()

    def rotate_ccw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index - 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self.current_orientation_display.setText(new_ori)
        current_pictograph = (
            self.ori_picker_box.graph_editor.GE_pictograph_view.pictograph
        )
        current_pictograph.updater.update_pictograph()
        self.current_sequence_json_handler.update_start_pos_ori(self.color, new_ori)
        self.json_validation_engine.run()
        self.ori_adjusted.emit(new_ori)
        current_pictograph.props[self.color].updater.update_prop({ORI: new_ori})
        current_pictograph.updater.update_pictograph()
        QApplication.processEvents()
        self.option_picker.update_option_picker()

    def resize_GE_start_pos_ori_picker_widget(self) -> None:
        button_size = int(self.ori_picker_box.height() // 4)
        icon_size = int(button_size * 0.6)
        for button in [self.ccw_button, self.cw_button]:
            button.setFixedSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))
        self._set_ori_label_font_size()
        self.set_current_orientation_display_font()

    def set_initial_orientation(
        self, start_pos_pictograph: Pictograph, color: str
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
        self.current_orientation_display.setText(initial_orientation)
