from settings.string_constants import ICON_DIR, SWAP_ICON
from PyQt6.QtGui import QIcon, QFont, QPainter, QPen
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, List, Locations, Colors
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_button import (
    CustomButton,
)
from widgets.graph_editor.pictograph.pictograph import Pictograph

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QBoxLayout,
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox

combobox_border = 2


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QComboBox {{
                border: {combobox_border}px solid black;
                border-radius: 10px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px; /* Width of the arrow */
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* Just a single line */
                border-top-right-radius: 3px; /* Same radius as QComboBox */
                border-bottom-right-radius: 3px;
            }}

            QComboBox::down-arrow {{
                image: url("resources/images/icons/combobox_arrow.png"); /* Path to your custom arrow icon */
                width: 10px; /* Width of the icon */
                height: 10px; /* Height of the icon */
            }}
        """
        )


class StartEndWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self.attr_box = attr_box
        self.combobox_width = int(self.attr_box.attr_box_width * 0.3)

        self._init_ui()

        ### SETUP UI ###

    def _init_ui(self) -> None:
        self._setup_main_layout()

        self.start_box = self._setup_start_end_box()
        self.end_box = self._setup_start_end_box()

        self.start_box_with_header_frame = self._create_box_with_header_frame(
            self.start_box, QVBoxLayout, "Start"
        )
        self.end_box_with_header_frame = self._create_box_with_header_frame(
            self.end_box, QVBoxLayout, "End"
        )

        self.button_frame = self._setup_button_frame()
        self.arrow_frame = self._setup_arrow_frame()

        self._add_widgets_to_layout()

        # self._add_borders()

    def _add_black_borders(self) -> None:
        self.setStyleSheet("border: 1px solid black;")
        self.button_frame.setStyleSheet("border: 1px solid black;")
        self.start_box_with_header_frame.setStyleSheet("border: 1px solid black;")
        self.end_box_with_header_frame.setStyleSheet("border: 1px solid black;")
        self.arrow_frame.setStyleSheet("border: 1px solid black;")

    def _setup_main_layout(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setFixedWidth(self.attr_box.attr_box_width)

    def _setup_start_end_box(self) -> CustomComboBox:
        start_end_box = CustomComboBox(self)
        start_end_box.addItems(["N", "E", "S", "W"])
        start_end_box.setFont(
            QFont("Arial", int(self.width() / 10), QFont.Weight.Bold, True)
        )
        start_end_box.setFixedSize(
            self.combobox_width,
            int(self.attr_box.attr_box_width * 0.2),
        )
        start_end_box.setCurrentIndex(-1)
        return start_end_box

    def _setup_arrow_frame(self) -> QFrame:
        arrow_label = self._setup_arrow_label()
        arrow_frame = QFrame(self)
        arrow_label.setContentsMargins(0, 0, 0, 0)

        arrow_frame_layout = QVBoxLayout(arrow_frame)
        arrow_frame_layout.setContentsMargins(0, 0, 0, 0)
        arrow_frame_layout.setSpacing(0)

        arrow_frame_layout.addSpacerItem(
            QSpacerItem(0, self.start_end_header_label.height())
        )
        arrow_frame_layout.addWidget(
            arrow_label,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        return arrow_frame

    def _setup_arrow_label(self) -> QFrame:
        arrow_label = QLabel("→", self)
        arrow_label.setFont(QFont("Arial", int(self.width() / 10), QFont.Weight.Bold))
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_label.setContentsMargins(0, 0, 0, 0)
        arrow_label.setFixedHeight(
            self.start_box.height() + self.attr_box.header_spacing
        )
        arrow_label.setFixedWidth(
            int(self.attr_box.attr_box_width / 5)
            - self.attr_box.border_width * 2
            - combobox_border
        )
        return arrow_label

    def _setup_start_end_header_label(self, label_text) -> QLabel:
        label = QLabel(label_text, self)
        label.setFont(QFont("Arial", int(self.width() / 14)))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setContentsMargins(0, 0, 0, 0)
        label.setFixedHeight(int(self.width() / 14) + self.attr_box.header_spacing)
        return label

    def _add_widgets_to_layout(self) -> None:
        self.main_layout.addWidget(self.button_frame)
        self.main_layout.addWidget(self.start_box_with_header_frame)
        self.main_layout.addWidget(self.arrow_frame)
        self.main_layout.addWidget(self.end_box_with_header_frame)

    ### CREATE WIDGETS ###

    def _setup_button_frame(self) -> QFrame:
        swap_button = self._create_button()
        button_frame = QFrame(self)
        button_frame.setFixedWidth(int(self.attr_box.attr_box_width * 1 / 5))
        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)

        button_size = int(self.attr_box.attr_box_width * 0.15)  # Example size
        swap_button.setFixedSize(button_size, button_size)
        button_frame_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        button_frame_layout.addWidget(
            swap_button,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        return button_frame
    
    def _create_button(self) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )  # Set size policy to fixed

        button.clicked.connect(self.swap_locations)
        return button

    def _create_box_with_header_frame(
        self, widget: QComboBox, layout_type, label_text
    ) -> QFrame:
        frame = QFrame(self)
        layout: QBoxLayout = layout_type(frame)

        layout.setSpacing(self.attr_box.header_spacing)
        layout.setContentsMargins(0, 0, 0, 0)
        frame.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame.setLayout(layout)
        self.start_end_header_label = self._setup_start_end_header_label(label_text)
        layout.addWidget(self.start_end_header_label)
        frame.setFixedWidth(self.combobox_width)
        layout.addWidget(widget)
        frame.setFixedHeight(
            int(
                self.start_end_header_label.height()
                + widget.height()
                + self.attr_box.header_spacing
            )
        )

        return frame

    ### CALLBACKS ###

    def swap_locations(self) -> None:
        start_index = self.start_box.currentIndex()
        end_index = self.end_box.currentIndex()
        self.start_box.setCurrentIndex(end_index)
        self.end_box.setCurrentIndex(start_index)
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.arrow.swap_rot_dir()

    ### UPDATE WIDGETS ###

    def clear_start_end_boxes(self) -> None:
        self.start_box.setCurrentIndex(-1)
        self.end_box.setCurrentIndex(-1)

    def update_start_end_boxes(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            self.start_box.setCurrentText(motion.start_location.upper())
            self.end_box.setCurrentText(motion.end_location.upper())

    def update_start_end_widget_size(self) -> None:
        self.setFixedHeight(
            int(
                self.start_box.height()
                + self.start_end_header_label.height()
                + self.attr_box.header_spacing
            )
        )
        self.setFixedWidth(self.attr_box.attr_box_width)
