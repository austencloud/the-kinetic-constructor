from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING

from Enums.letters import LetterType
from constants import BLUE, CLOCKWISE, COUNTER_CLOCKWISE, RED
from widgets.factories.button_factory.buttons.letterbook_adjust_turns_button import (
    LetterBookAdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import (
        GE_TurnsBox,
    )


class GE_TurnsBoxHeader(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header_label()
        self._setup_layout()
        self._add_widgets()

        self.update_turns_box_header()

    def update_turns_box_header(self) -> None:
        """This is called every time the GE pictograph scene is updated in order to display the correct buttons."""
        pictograph = self.turns_box.graph_editor.GE_pictograph_view.pictograph
        letter_type = None
        motion = pictograph.get.motion_by_color(self.turns_box.color)
        turns = motion.turns
        is_shift = motion.check.is_shift()
        prop_rot_dir_button_mngr = self.turns_box.prop_rot_dir_button_manager
        if pictograph.letter:
            letter_type = LetterType.get_letter_type(pictograph.letter)
        if letter_type == LetterType.Type1 or letter_type == None:
            self.turns_box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
            self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()
        else:
            if letter_type == LetterType.Type2 or letter_type == LetterType.Type3:
                if turns and not is_shift:
                    self.turns_box.vtg_dir_button_manager.show_vtg_dir_buttons()
                    if pictograph.red_motion.turns and pictograph.blue_motion.turns:
                        if (
                            pictograph.red_motion.prop_rot_dir
                            == pictograph.blue_motion.prop_rot_dir
                        ):
                            self.turns_box.vtg_dir_button_manager.same_button.press()
                        else:
                            self.turns_box.vtg_dir_button_manager.opp_button.press()
                else:
                    self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()
            else:
                if turns:
                    prop_rot_dir_button_mngr.show_prop_rot_dir_buttons()
                    if motion.prop_rot_dir == CLOCKWISE:
                        prop_rot_dir_button_mngr.cw_button.press()
                    elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                        prop_rot_dir_button_mngr.ccw_button.press()
                else:
                    prop_rot_dir_button_mngr.hide_prop_rot_dir_buttons()
        QApplication.processEvents()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.top_hbox = QHBoxLayout()
        self.bottom_hbox = QHBoxLayout()
        self.layout.addLayout(self.top_hbox)
        self.layout.addLayout(self.bottom_hbox)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set size policy to Fixed
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.ccw_button)
        self.top_hbox.addWidget(self.turns_box.vtg_dir_button_manager.opp_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.vtg_dir_button_manager.same_button)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.cw_button)
        self.top_hbox.addStretch(1)
        self.bottom_hbox.addWidget(self.separator)

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_header_label(self) -> QLabel:
        self.header_label = QLabel(self)
        color = self.turns_box.color
        text = ""

        if color == RED:
            text = "Right"
            font_color = QColor("#ED1C24")
        elif color == BLUE:
            text = "Left"
            font_color = QColor("#2E3192")

        self.header_label_font = QFont("Arial")
        self.header_label_font.setBold(True)
        self.header_label.setFont(self.header_label_font)
        self.header_label.setText(text)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet(f"color: {font_color.name()};")
        return self.header_label

    def _resize_header_label(self) -> None:
        font_size = self.graph_editor.width() // 40
        self.header_label_font.setPointSize(font_size)
        self.header_label.setFont(self.header_label_font)
        self.header_label.repaint()

    def create_attr_header_label(
        self, text: str, align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ) -> QLabel:
        attr_label = QLabel(text, self)
        attr_label.setFont(QFont("Arial"))
        attr_label.setAlignment(align)
        attr_label.setContentsMargins(0, 0, 0, 0)
        return attr_label

    def create_header_frame(self, layout: QHBoxLayout | QHBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_adjust_turns_button(self, text: str) -> LetterBookAdjustTurnsButton:
        button = LetterBookAdjustTurnsButton(self)
        button.setText(text)
        return button

    def resize_GE_turns_box_header(self) -> None:
        self.setFixedHeight(self.turns_box.height() // 4)
        self._resize_header_label()
