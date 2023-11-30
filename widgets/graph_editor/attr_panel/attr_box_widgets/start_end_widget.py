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
    def __init__(self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox") -> None:
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

        # Button Frame
        button_frame = QFrame(self)
        button_layout = QVBoxLayout(button_frame)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.swap_button = self._create_button()
        button_layout.addWidget(self.swap_button)
        button_frame.setFixedWidth(int(self.attr_box.attr_box_width / 4))

        # Combo Boxes        
        self.start_combo_box = self.create_combo_box()
        self.end_combo_box = self.create_combo_box()
        
        start_combo_frame = self._create_combo_frame("Start", self.start_combo_box)
        end_combo_frame = self._create_combo_frame("End", self.end_combo_box)

        # Arrow Label
        arrow_frame = QFrame()
        arrow_frame_layout = QVBoxLayout(arrow_frame)
        self.arrow_label = QLabel("→", self)
        self.arrow_label.setFont(QFont("Arial", 20, QFont.Weight.Bold, True))
        self.arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.arrow_label.setContentsMargins(0, 0, 0, 0)  # No margins
        arrow_frame_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        arrow_frame_layout.setSpacing(0)  # No extra spacing
        arrow_frame_layout.addSpacing(int(self.start_combo_box.height()/2))  # Move arrow text down
        arrow_frame_layout.addWidget(self.arrow_label)

        # Add layouts to the main layout
        main_layout.addWidget(button_frame)
        main_layout.addWidget(start_combo_frame)
        main_layout.addWidget(arrow_frame)
        main_layout.addWidget(end_combo_frame)

        
    def _create_combo_frame(self, label_text, combo_box) -> QFrame:
        layout = QVBoxLayout()
        layout.setSpacing(0)  # No extra spacing
        layout.setContentsMargins(0, 0, 0, 0)  # No margins

        label = QLabel(label_text, self)
        label.setFont(QFont("Arial", 12))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setContentsMargins(0, 0, 0, 0)  # No margins on label
        label.setFixedHeight(int(self.start_combo_box.height()/2))

        layout.addWidget(label)
        layout.addWidget(combo_box)
        frame = QFrame()
        frame.setLayout(layout)

        return frame

    def create_combo_box(self):
        combo_box = CustomComboBox(self)
        combo_box.addItems(["N", "E", "S", "W"])
        combo_box.setFont(QFont("Arial", 20, QFont.Weight.Bold, True))
        return combo_box


    ### CREATE WIDGETS ###

    def _create_button(self) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setStyleSheet(
            "QPushButton {"
            "   border-radius: 15px;"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            "   border: 1px solid black;"
            "   min-width: 30px;"
            "   min-height: 30px;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )
        button.setFixedSize(30, 30)
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
        self.setFixedHeight(self.start_combo_box.height() * 2)
