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
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from Enums.MotionAttributes import Color
from Enums.letters import LetterType
from widgets.factories.button_factory.buttons.codex_adjust_turns_button import (
    CodexAdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import (
        GE_TurnsBox,
    )


class GE_TurnsBoxHeader(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)

        self.turns_box = turns_box
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header_label()
        self._setup_layout()
        self._add_widgets()

        self.update_turns_box_header()

    def update_turns_box_header(self) -> None:
        """This is called every time the GE pictograph scene is updated in order to display the correct buttons."""
        letter_type = self.turns_box.pictograph.letter_type
        if letter_type == LetterType.Type1 or letter_type == None:
            self.turns_box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
            self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()
        else:
            self.turns_box.prop_rot_dir_button_manager.show_prop_rot_dir_buttons()
            self.turns_box.vtg_dir_button_manager.show_vtg_dir_buttons()
        QApplication.processEvents()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.top_hbox = QHBoxLayout()
        self.bottom_hbox = QHBoxLayout()
        self.layout.addLayout(self.top_hbox)
        self.layout.addLayout(self.bottom_hbox)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

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
        color = self.turns_box.color
        text = ""
        font_color = "#000000"

        if color == Color.RED:
            text = "Right"
            font_color = "#ED1C24"
        elif color == Color.BLUE:
            text = "Left"
            font_color = "#2E3192"

        font_size = self.turns_box.width() // 3
        font_weight = "bold"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )

        return label

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

    def create_adjust_turns_button(self, text: str) -> CodexAdjustTurnsButton:
        button = CodexAdjustTurnsButton(self)
        button.setText(text)
        return button
