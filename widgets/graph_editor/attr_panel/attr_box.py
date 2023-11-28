import logging
from typing import TYPE_CHECKING, Literal, Dict
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QWidget,
    QHBoxLayout,
)
from objects.arrow import Arrow
from objects.motion import Motion
from settings.string_constants import (
    ANTI,
    BLUE,
    PRO,
    RED,
    STATIC,
    ICON_PATHS,
    RED_HEX,
    BLUE_HEX,
)
from utilities.TypeChecking.TypeChecking import Color

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_panel import (
        AttrPanel,
    )
from PyQt6.QtWidgets import QSizePolicy
from widgets.graph_editor.attr_panel.attr_box_widgets import (
    StartEndWidget,
    MotionTypeWidget,
    TurnsWidget,
    HeaderWidget,
)


class AttrBox(QFrame):
    def __init__(
        self, attr_panel: 'AttrPanel', pictograph: 'Pictograph', color: Color
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.turns_widget = None
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self) -> None:
        self.setup_box()
        self.button_size = self.calculate_button_size()
        self.icon_size = QSize(int(self.button_size * 0.5), int(self.button_size * 0.5))

        # self.attribute_labels = self.create_attribute_labels()

        self.header_widget = HeaderWidget(self, self.color)
        self.motion_type_widget = MotionTypeWidget(self)
        self.start_end_widget = StartEndWidget(self)
        self.turns_widget = TurnsWidget(self.pictograph, self.color, self)

        self.turns_widget.subtract_turns_button.setIconSize(self.icon_size)
        self.turns_widget.add_turns_button.setIconSize(self.icon_size)
        self.turns_widget.subtract_turns_button.setFixedSize(
            self.button_size, self.button_size
        )
        self.turns_widget.add_turns_button.setFixedSize(
            self.button_size, self.button_size
        )
        self.clock_label = self.create_clock_label()
        self.apply_button_styles()

        self.preload_pixmaps()

        self.layout().addWidget(self.header_widget)
        self.layout().addWidget(self.motion_type_widget)
        self.layout().addWidget(self.start_end_widget)
        self.layout().addWidget(self.turns_widget)

    def apply_button_styles(self) -> None:
        button_style = (
            'QPushButton {'
            '   border-radius: 15px;'
            '   background-color: #f0f0f0;'
            '   border: 1px solid #a0a0a0;'
            '   min-width: 30px;'
            '   min-height: 30px;'
            '}'
            'QPushButton:pressed {'
            '   background-color: #c0c0c0;'
            '}'
        )
        if self.turns_widget:
            self.turns_widget.subtract_turns_button.setStyleSheet(button_style)
            self.turns_widget.add_turns_button.setStyleSheet(button_style)

    def setup_box(self) -> None:
        self.setObjectName('AttributeBox')
        self.apply_border_style(RED_HEX if self.color == RED else BLUE_HEX)
        self.setFixedSize(
            int(self.attr_panel.width()), int(self.attr_panel.height() / 2)
        )
        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(f'#AttributeBox {{ border: 3px solid {color_hex}; }}')

    ### CREATE LABELS ###

    def create_attribute_labels(self) -> Dict[str, QLabel]:
        labels = {}
        for name in [
            'motion_type_label',
            'start_end_label',
        ]:
            label = self.create_label(self.height() // 4)
            label.setObjectName(name)
            labels[name] = label
        return labels

    def create_label(self, height: int) -> QLabel:
        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(self.width(), height)
        return label

    def create_clock_label(self) -> QLabel:
        label = self.create_label(self.height() // 4)
        label.setObjectName('clock_label')
        return label

    def add_labels_to_layout(self) -> None:
        self.layout().addWidget(self.info_header)
        for label in self.attribute_labels.values():
            self.layout().addWidget(label)
        self.layout().addWidget(self.turns_widget)

    def setup_button_column(
        self, x_position: int, button_names: list, column: Literal['left', 'right']
    ) -> None:
        button_column = QFrame(self)
        button_column_layout = QVBoxLayout(button_column)
        button_column_layout.setContentsMargins(0, 0, 0, 0)
        button_column_layout.setSpacing(0)

        button_column.setFixedSize(self.button_size, self.height())
        button_column.move(x_position, 0)

        if column == 'left':
            top_spacer = QSpacerItem(
                self.button_size,
                self.button_size,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Expanding,
            )
            button_column_layout.addItem(top_spacer)

        if column == 'right':
            button_column_layout.addWidget(self.clock_label)

        middle_spacer = QSpacerItem(
            self.button_size,
            self.button_size,
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )
        button_column_layout.addItem(middle_spacer)

        if column == 'left':
            for button_name in button_names:
                button = self.create_button(
                    ICON_PATHS[button_name], getattr(self, f'{button_name}_callback')
                )
                button_column_layout.addWidget(button)

        if column == 'right' and 'add_turns' in button_names:
            add_turns_button = self.create_button(
                ICON_PATHS['add_turns'], self.add_turns_callback
            )
            button_column_layout.addWidget(add_turns_button)

        button_column.raise_()
        return button_column

    def create_button(self, icon_path, callback):
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(self.icon_size)
        button.setFixedSize(self.button_size, self.button_size)
        button.clicked.connect(callback)

        # Return the button without setting a stylesheet
        return button

    def swap_motion_type_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_motion_type()
            self.update_labels(arrow)

    def swap_start_end_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_rot_dir()
            self.update_labels(arrow)

    def subtract_turns_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.subtract_turn()
            self.update_labels(arrow)

    def add_turns_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.add_turn()
            self.update_labels(arrow)

    def preload_pixmaps(self) -> None:
        for icon_name, icon_path in ICON_PATHS.items():
            if not icon_path:
                logging.warning(f'No file path specified for icon '{icon_name}'.')
                continue
            pixmap = QPixmap(icon_path)
            if pixmap.isNull():
                logging.error(
                    f'Failed to load icon '{icon_name}' from path '{icon_path}'.'
                )
                continue
            scaled_pixmap = pixmap.scaled(
                self.button_size,
                self.button_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.pixmap_cache[icon_name] = scaled_pixmap

    def set_clock_pixmap(self, clock_label: QLabel, icon_name: str) -> None:
        if icon_name not in self.pixmap_cache:
            logging.error(f'Icon name '{icon_name}' not found in pixmap cache.')
            return
        pixmap = self.pixmap_cache[icon_name]
        if pixmap.isNull():
            logging.error(f'Pixmap for icon name '{icon_name}' is null.')
            return
        clock_label.setPixmap(pixmap)

    def update_attr_box(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            self.update_labels(arrow)

    def update_labels(self, motion: 'Motion') -> None:
        self.turns_widget.turns_label.setText(f'{motion.turns}')

    def update_attr_box_size(self) -> None:
        self.setFixedHeight(int(self.attr_panel.pictograph.graph_editor.height() / 2))
        self.setFixedWidth(int(self.attr_panel.pictograph.graph_editor.height() / 2))
        # delete the buttons layouts
        for child in self.children():
            if isinstance(child, QFrame):
                child.deleteLater()

        if self.turns_widget:
            for child in self.turns_widget.children():
                if isinstance(child, QFrame):
                    child.deleteLater()
        self.init_ui()
        self.header_widget.setup_header_widget()
        self.update()
