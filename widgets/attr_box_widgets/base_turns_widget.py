from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, List, Union
from widgets.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from widgets.attr_box_widgets.attr_box_button import AttrBoxButton
from widgets.attr_panel.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_turns_widget import GraphEditorTurnsWidget
    from widgets.ig_tab.ig_filter_tab.ig_turns_widget.ig_motion_type_turns_widget import IGMotionTypeTurnsWidget


class BaseTurnsWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        self.attr_box = attr_box
        super().__init__(attr_box)
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.turns_display = self.create_turns_display()
        self.add_subtract_buttons = self._setup_add_subtract_turns_buttons()
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

        self.main_hbox_layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def _add_frames_to_main_layout(self) -> None:
        main_frame = QFrame()
        main_frame.setLayout(self.main_hbox_layout)
        self.main_hbox_layout.addWidget(self.subtract_button_frame)
        self.main_hbox_layout.addWidget(self.turns_display_frame)
        self.main_hbox_layout.addWidget(self.add_button_frame)
        self.layout.addWidget(main_frame)

    def _setup_add_subtract_turns_buttons(self) -> List[AttrBoxButton]:
        self.subtract_turns_buttons = [
            self._create_turns_button(text) for text in ["-1", "-0.5"]
        ]
        self.add_turns_buttons = [
            self._create_turns_button(text) for text in ["+0.5", "+1"]
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

    def _create_turns_button(
        self, text: str
    ) -> AttrBoxButton:
        button = AttrBoxButton(self)
        button.setText(text)
        turn_adjustment_mapping = {"-1": -1, "-0.5": -0.5, "+0.5": 0.5, "+1": 1}
        turn_adjustment = turn_adjustment_mapping.get(text, 0)
        button.clicked.connect(lambda: self._adjust_turns(turn_adjustment))
        return button

    def _get_turns_display_style_sheet(self) -> str:
        return """
            QLabel {
                border: 1px solid #c0c0c0;
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

    def _adjust_turns(self, adjustment: float) -> None:
        # This method should be implemented in the subclasses where it's needed.
        pass

    def set_layout_margins_and_alignment(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        """Convert turn values from string to numeric."""
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)