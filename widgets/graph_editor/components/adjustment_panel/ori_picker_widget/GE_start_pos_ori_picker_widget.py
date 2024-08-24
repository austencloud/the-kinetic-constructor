from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint
from data.constants import IN, ORI, OUT, CLOCK, COUNTER
from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path
from widgets.pictograph.pictograph import Pictograph

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)


from widgets.graph_editor.components.adjustment_panel.ori_picker_widget.GE_ori_picker_display_manager import (
    GE_OriPickerDisplayManager,
)
from widgets.graph_editor.components.adjustment_panel.ori_picker_widget.GE_orientation_selection_dialog import (
    GE_OrientationSelectionDialog,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.adjustment_panel.start_pos_ori_picker_box.GE_start_pos_ori_picker_box import (
        GE_StartPosOriPickerBox,
    )


class GE_StartPosOriPickerWidget(QWidget):
    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "GE_StartPosOriPickerBox") -> None:
        super().__init__()
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color
        self.main_widget = self.ori_picker_box.graph_editor.main_widget
        self.current_orientation_index = 0
        self.orientations = [IN, COUNTER, OUT, CLOCK]
        self.json_manager = self.main_widget.json_manager
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame
        self.json_validation_engine = self.main_widget.json_manager.validation_engine
        self.option_picker = (
            self.beat_frame.sequence_widget.top_builder_widget.sequence_builder.option_picker
        )
        self._setup_current_ori_display()
        self._setup_orientation_label()
        self._setup_orientation_control_layout()

        self.display_manager = GE_OriPickerDisplayManager(self)
        self.ori_adjusted.connect(self.beat_frame.on_beat_adjusted)
        self._setup_layout()

    def _setup_current_ori_display(self) -> None:
        self.ori_display_label = QLabel()
        self.ori_display_label_layout = QHBoxLayout()
        self.ori_display_label_layout.addStretch(1)
        self.ori_display_label_layout.addWidget(self.ori_display_label)
        self.ori_display_label_layout.addStretch(1)

    def _setup_layout(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.ori_label, 1)
        self.main_layout.addLayout(self.ori_display_label_layout, 2)
        self.main_layout.addLayout(self.orientation_control_layout, 10)

    def on_orientation_display_clicked(self, event) -> None:
        dialog = GE_OrientationSelectionDialog(self)
        dialog.move(self.mapToGlobal(QPoint(0, 0)))
        if dialog.exec():
            new_orientation = dialog.selected_orientation
            self.set_orientation(new_orientation)

    def _setup_orientation_label(self) -> None:
        self.ori_label = QLabel("Orientation")
        self.ori_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _set_ori_label_font_size(self) -> None:
        ori_label_font_size = self.ori_picker_box.graph_editor.width() // 60
        font = QFont("Cambria", ori_label_font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.ori_label.setFont(font)

    def _setup_orientation_control_layout(self) -> None:
        path = get_images_and_data_path("images/icons")
        self.ccw_button = self.setup_button(f"{path}/rotate_ccw.png", self.rotate_ccw)
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
        # make the cursor a pointing hand when hovering over the button
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def set_orientation(self, orientation):
        self.current_orientation_index = self.orientations.index(orientation)
        self.ori_display_label.setText(orientation)
        self.json_manager.start_position_handler.update_start_pos_ori(
            self.color, orientation
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.ori_adjusted.emit(orientation)
        current_pictograph = (
            self.ori_picker_box.graph_editor.GE_pictograph_view.pictograph
        )
        current_pictograph.props[self.color].updater.update_prop({ORI: orientation})
        current_pictograph.updater.update_pictograph()
        QApplication.processEvents()
        self.option_picker.update_option_picker()

    def rotate_cw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index + 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self._rotate_orientation(new_ori)

    def rotate_ccw(self) -> None:
        self.current_orientation_index = (self.current_orientation_index - 1) % len(
            self.orientations
        )
        new_ori = self.orientations[self.current_orientation_index]
        self._rotate_orientation(new_ori)

    def _rotate_orientation(self, new_ori: str) -> None:
        self.ori_display_label.setText(new_ori)
        current_pictograph = (
            self.ori_picker_box.graph_editor.GE_pictograph_view.pictograph
        )
        self.json_manager.start_position_handler.update_start_pos_ori(
            self.color, new_ori
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.ori_adjusted.emit(new_ori)
        current_pictograph.props[self.color].updater.update_prop({ORI: new_ori})
        current_pictograph.updater.update_pictograph()
        QApplication.processEvents()
        self.option_picker.update_option_picker()

    def resize_GE_start_pos_ori_picker_widget(self) -> None:
        self._set_button_size()
        self._set_ori_label_font_size()
        self.display_manager.set_ori_display_font_size()
        self.display_manager.set_label_styles()

    def _set_button_size(self):
        button_size = int(self.ori_picker_box.height() // 4)
        icon_size = int(button_size * 0.6)
        for button in [self.ccw_button, self.cw_button]:
            button.setFixedSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))

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
        self.ori_display_label.setText(initial_orientation)
