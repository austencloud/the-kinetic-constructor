from settings.string_constants import ICON_DIR, SWAP_ICON
from PyQt6.QtGui import QIcon, QFont, QPainter, QPen
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, List, Locations, Colors
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
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QComboBox {
                border: 2px solid black;
                border-radius: 10px;

            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px; /* Width of the arrow */
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* Just a single line */
                border-top-right-radius: 3px; /* Same radius as QComboBox */
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                image: url("resources/images/icons/combobox_arrow.png"); /* Path to your custom arrow icon */
                width: 10px; /* Width of the icon */
                height: 10px; /* Height of the icon */
            }
        """
        )


class StartEndWidget(QWidget):
    def __init__(
        self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox"
    ) -> None:
        super().__init__(attr_box)
        self.pictograph = pictograph
        self.color = color
        self.attr_box = attr_box

        self._setup_ui()

    def _setup_ui(self) -> None:
        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setFixedHeight(int(self.attr_box.height() * 1 / 8))

        button_frame = self.setup_button_frame()
        combobox_frame = self.setup_combo_frame()
    
        main_layout.addWidget(button_frame)
        main_layout.addWidget(combobox_frame)

    def setup_button_frame(self):
        button_frame = QFrame(self)
        button_layout = QVBoxLayout(button_frame)
        button_frame.setContentsMargins(0, 0, 0, 0)  # No margins
        button_layout.setSpacing(0)  # No extra spacing
        button_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.swap_button = self._create_button()
        button_spacer = QFrame()
        button_spacer.setFixedHeight(int(self.width() * 1 / 8))
        button_layout.addWidget(button_spacer)
        button_layout.addWidget(self.swap_button)
        button_frame.setFixedWidth(int(self.attr_box.attr_box_width / 4))
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return button_frame

    def setup_arrow_frame(self):
        arrow_frame = QFrame()
        arrow_frame_layout = QVBoxLayout(arrow_frame)
        self.arrow_label = QLabel("→", self)
        self.arrow_label.setFont(QFont("Arial", 16, QFont.Weight.Bold, True))
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.arrow_label.setContentsMargins(0, 0, 0, 0)  # No margins
        arrow_frame_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        arrow_frame_layout.setSpacing(0)  # No extra spacing
        arrow_frame_layout.addSpacing(int(self.width() * 1 / 8))
        arrow_frame_layout.addWidget(self.arrow_label)
        return arrow_frame

    def setup_combo_frame(self):
        arrow_frame = self.setup_arrow_frame()
        self.start_combo_box = self.create_combo_box()
        self.end_combo_box = self.create_combo_box()
        start_combo_frame = self._create_combo_frame("Start", self.start_combo_box)
        end_combo_frame = self._create_combo_frame("End", self.end_combo_box)
        combobox_layout = QHBoxLayout()
        combobox_layout.addWidget(start_combo_frame)
        combobox_layout.addWidget(arrow_frame)
        combobox_layout.addWidget(end_combo_frame)
        combobox_layout.setSpacing(0)
        combobox_frame = QFrame()
        combobox_frame.setLayout(combobox_layout)
        combobox_frame.setContentsMargins(0, 0, 0, 0)
        combobox_layout.setContentsMargins(0, 0, 0, 0)
        return combobox_frame

    def _create_combo_frame(self, label_text, combo_box) -> QFrame:
        combo_frame_layout = QVBoxLayout()

        self.combo_box_label = QLabel(label_text, self)
        self.combo_box_label.setFont(QFont("Arial", 12))
        self.combo_box_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.combo_box_label.setContentsMargins(0, 0, 0, 0)  # No margins on label
        self.combo_box_label.setFixedHeight(int(self.width() * 1 / 8))
        
        combo_frame_layout.setSpacing(0)  # No extra spacing
        combo_frame_layout.setContentsMargins(0, 0, 0, 0)  # No margins

        combo_frame_layout.addWidget(self.combo_box_label)
        combo_frame_layout.addWidget(combo_box)

        combo_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame.setLayout(combo_frame_layout)

        return frame

    def create_combo_box(self):
        combo_box = CustomComboBox(self)
        combo_box.addItems(["N", "E", "S", "W"])
        combo_box.setFont(QFont("Arial", 20, QFont.Weight.Bold, True))
        combo_box.setFixedSize(
            int(self.attr_box.attr_box_width * 0.3),
            int(self.attr_box.attr_box_width * 0.2),
        )
        return combo_box

    ### CREATE WIDGETS ###

    def _create_button(self) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setStyleSheet(
            "QPushButton {"
            f"   border-radius: {int(self.attr_box.attr_box_width * 0.15 / 2)};"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            "   border: 1px solid black;"
            f"   min-width: {self.attr_box.attr_box_width * 0.15}px;"
            f"   min-height: {self.attr_box.attr_box_width * 0.15}px;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )
        button.setFixedSize(
            int(self.attr_box.attr_box_width * 0.3),
            int(self.attr_box.attr_box_width * 0.3),
        )
        button.clicked.connect(self.swap_locations)
        return button

    def _create_layout(self, *widgets) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    ### CONNECT SIGNALS ###

    def swap_locations(self) -> None:
        start_index = self.start_combo_box.currentIndex()
        end_index = self.end_combo_box.currentIndex()
        self.start_combo_box.setCurrentIndex(end_index)
        self.end_combo_box.setCurrentIndex(start_index)
        self.update_arrow_rotation_direction()

    ### UPDATE ###

    def update_combo_boxes(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            self.start_combo_box.setCurrentText(motion.start_location.upper())
            self.end_combo_box.setCurrentText(motion.end_location.upper())

    def update_arrow_rotation_direction(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_rot_dir()

    def update_start_end_widget_size(self) -> None:
        self.setFixedHeight(
            int(self.start_combo_box.height() + self.combo_box_label.height()) + 3
        )
