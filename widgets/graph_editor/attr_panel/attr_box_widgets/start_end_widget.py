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

    ### SETUP ###

    def _setup_ui(self) -> None:
        # Set up the UI components and layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setFixedWidth(int(self.attr_box.width()))
        self.setFixedHeight(int(self.attr_box.height() * 1 / 6))

        locations: List[Locations] = ["N", "E", "S", "W"]
        self._setup_labels(locations)
        self._setup_buttons(locations)
        self._setup_layouts()

    def _setup_labels(self, locations: List[Locations]) -> None:
        # Set up labels and combo boxes
        start_end_font = QFont("Arial", 12)
        font = QFont("Arial", 20, weight=QFont.Weight.Bold, italic=True)

        self.start_label = self._create_label("Start", start_end_font)
        self.start_combo_box = self._create_combo_box(locations, font)

        self.arrow_label = self._create_label("→", font)

        self.end_label = self._create_label("End", start_end_font)
        self.end_combo_box = self._create_combo_box(locations, font)

    def _setup_buttons(self, locations: List[Locations]) -> None:
        # Set up buttons
        combo_box_height = int(self.width() * 0.2)
        self.swap_button = self._create_button(combo_box_height)
        self.swap_button.clicked.connect(self.swap_locations)

    def _setup_layouts(self) -> None:
        self.start_layout = self._create_layout(self.start_label, self.start_combo_box)
        self.bottom_spacer = QSpacerItem(
            0, self.height() - self.start_combo_box.height()
        )

        self.arrow_button_layout = QVBoxLayout()
        self.arrow_button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.arrow_button_layout.addWidget(self.swap_button)
        self.arrow_button_layout.addWidget(self.arrow_label)
        self.arrow_button_layout.addItem(self.bottom_spacer)

        self.end_layout = self._create_layout(self.end_label, self.end_combo_box)

        self.start_end_layout = QHBoxLayout()
        self.start_end_layout.setSpacing(10)
        self.start_end_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_end_layout.addLayout(self.start_layout)
        self.start_end_layout.addLayout(self.arrow_button_layout)
        self.start_end_layout.addLayout(self.end_layout)

        self.layout.addLayout(self.start_end_layout)

    ### CREATE WIDGETS ###

    def _create_label(self, text: str, font: QFont) -> QLabel:
        label = QLabel(text, self)
        label.setFont(font)
        label.setFixedHeight(int(self.width() * 0.2 / 2))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _create_combo_box(
        self, locations: List[Locations], font: QFont
    ) -> CustomComboBox:
        combo_box = CustomComboBox(self)
        combo_box.addItems(locations)
        combo_box.setFont(font)
        combo_box.setFixedSize(int(self.width() * 0.2 + 15), int(self.width() * 0.2))
        return combo_box

    def _create_button(self, size: int) -> QPushButton:
        button = QPushButton(self)
        button.setStyleSheet(self.attr_box.get_button_style())
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setFixedSize(int(size / 2), int(size / 2))
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
        self.setFixedSize(
            self.attr_box.attr_box_width,
            int(self.attr_box.height() * 1 / 6),
        )
