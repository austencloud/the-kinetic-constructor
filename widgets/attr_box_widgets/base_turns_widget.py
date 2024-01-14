from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import List, Union
from widgets.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from widgets.attr_box_widgets.attr_box_button import AttrBoxButton
from widgets.attr_panel.base_attr_box import BaseAttrBox


class BaseTurnsWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        self.attr_box = attr_box
        super().__init__(attr_box)

    def _initialize_ui(self) -> None:
        self.turns_display = self.create_turns_display()
        self.adjust_turns_buttons = self._setup_adjust_turns_buttons()
        self._setup_layout()
        self._create_frames()
        self._add_frames_to_main_layout()
        self.setup_turns_label()
        self.setup_turns_display()

    def setup_turns_label(self) -> None:
        self.turns_label = QLabel("Turns", self)
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_display_frame.layout().addWidget(self.turns_label)

    def setup_turns_display(self) -> None:
        self.turns_display_frame.layout().addWidget(self.turns_display)
        self.set_layout_margins_and_alignment()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def _add_frames_to_main_layout(self) -> None:
        turn_display_and_adjust_btns_frame = QFrame()
        turn_display_and_adjust_btns_frame.setLayout(
            self.turn_display_and_adjust_btns_hbox_layout
        )
        self.turn_display_and_adjust_btns_hbox_layout.addWidget(
            self.subtract_button_frame
        )
        self.turn_display_and_adjust_btns_hbox_layout.addWidget(
            self.turns_display_frame
        )
        self.turn_display_and_adjust_btns_hbox_layout.addWidget(self.add_button_frame)
        self.layout.addWidget(turn_display_and_adjust_btns_frame)

    def _setup_adjust_turns_buttons(self) -> List[AttrBoxButton]:
        self.subtract_turns_buttons = [
            self._create_adjust_turns_button(text) for text in ["-1", "-0.5"]
        ]
        self.add_turns_buttons = [
            self._create_adjust_turns_button(text) for text in ["+1", "+0.5"]
        ]
        turns_buttons = self.subtract_turns_buttons + self.add_turns_buttons
        return turns_buttons

    def _configure_layout(self, layout: QVBoxLayout):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)

    def create_turns_display(self) -> QLabel:
        turns_display = QLabel("0", self)
        turns_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_display.setStyleSheet(self._get_turns_display_style_sheet())
        turns_display.setFont(QFont("Arial", 16))
        return turns_display

    def _create_frames(self) -> None:
        self.turns_display_frame = self.create_turns_display_frame(QVBoxLayout())
        self.subtract_button_frame = self.create_button_frame(
            self.subtract_turns_buttons
        )
        self.add_button_frame = self.create_button_frame(self.add_turns_buttons)

    def create_turns_display_frame(self, layout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        self._configure_layout(layout)
        return frame

    def create_button_frame(self, buttons) -> QFrame:
        frame = QFrame()
        layout = QVBoxLayout(frame)
        self._configure_layout(layout)
        for button in buttons:
            layout.addWidget(button)
        return frame

    def _create_adjust_turns_button(self, text: str) -> AttrBoxButton:
        button = AttrBoxButton(self)
        button.setText(text)
        turn_adjustment_mapping = {"-1": -1, "-0.5": -0.5, "+0.5": 0.5, "+1": 1}
        turn_adjustment = turn_adjustment_mapping.get(text, 0)
        button.clicked.connect(lambda: self._adjust_turns(turn_adjustment))


        return button

    def _get_turns_display_style_sheet(self) -> str:
        return """
            QLabel {
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel:hover {
                background-color: #e5e5e5;
            }
        """

    def _get_direct_set_button_style_sheet(self) -> str:
        """Get the style sheet for the direct set turns buttons."""
        return """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e5e5e5;
                border-color: #a0a0a0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


    def set_layout_margins_and_alignment(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        """Convert turn values from string to numeric."""
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)


    def update_turnbox_size(self) -> None:
        """Update the size of the turns display for motion type."""
        self.spacing = self.attr_box.attr_panel.height() // 250
        border_radius = (
            min(self.turns_display.width(), self.turns_display.height()) * 0.25
        )
        turns_display_font_size = int(self.attr_box.height() / 8)

        self.turns_display.setMinimumHeight(int(self.attr_box.height() / 3))
        self.turns_display.setMaximumHeight(int(self.attr_box.height() / 3))
        self.turns_display.setMinimumWidth(int(self.attr_box.height() / 3))
        self.turns_display.setMaximumWidth(int(self.attr_box.height() / 3))
        self.turns_display.setFont(
            QFont("Arial", turns_display_font_size, QFont.Weight.Bold)
        )

        # Adjust the stylesheet to match the combo box style without the arrow
        self.turns_display.setStyleSheet(
            f"""
            QLabel {{
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def update_adjust_turns_button_size(self) -> None:
        for button in self.adjust_turns_buttons:
            button_size = self.calculate_adjust_turns_button_size()
            button.update_attr_box_adjust_turns_button_size(button_size)

    def calculate_adjust_turns_button_size(self) -> int:
        return int(self.attr_box.height() / 6)