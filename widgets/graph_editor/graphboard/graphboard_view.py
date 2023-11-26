from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from settings.string_constants import CLOCKWISE, COUNTER_CLOCKWISE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
from PyQt6.QtCore import QSize


class GraphBoardView(QGraphicsView):
    def __init__(self, graphboard: "GraphBoard") -> None:
        super().__init__()
        self.graphboard = graphboard

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.graphboard)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None

        # Initialize buttons
        self.init_buttons()

    def init_buttons(self):
        self.add_to_sequence_button = self.create_button(
            "resources/images/icons/add_to_sequence.png",
            self.graphboard.add_to_sequence,
        )
        self.clear_button = self.create_button(
            "resources/images/icons/clear.png", self.graphboard.clear_graphboard
        )
        self.rotate_clockwise_button = self.create_button(
            "resources/images/icons/rotate_right.png",
            lambda: self.graphboard.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_counterclockwise_button = self.create_button(
            "resources/images/icons/rotate_left.png",
            lambda: self.graphboard.rotate_pictograph(COUNTER_CLOCKWISE),
        )

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def update_graphboard_size(self) -> None:
        view_width = int(self.graphboard.graph_editor.height() * 75 / 90)
        self.setFixedWidth(view_width)
        self.setFixedHeight(self.graphboard.graph_editor.height())
        view_scale = view_width / self.graphboard.width()
        self.resetTransform()
        self.scale(view_scale, view_scale)

        button_size = int(self.width() / 7)
        self.configure_button_size_and_position(
            self.add_to_sequence_button, button_size
        )
        self.configure_button_size_and_position(self.clear_button, button_size)
        self.configure_button_size_and_position(
            self.rotate_clockwise_button, button_size
        )
        self.configure_button_size_and_position(
            self.rotate_counterclockwise_button, button_size
        )

    def configure_button_size_and_position(self, button: QPushButton, size) -> None:
        button.setFixedSize(size, size)
        icon_size = int(size * 0.8)
        button.setIconSize(QSize(icon_size, icon_size))

        # Custom positioning logic if needed
        if button == self.add_to_sequence_button:
            button.move(self.width() - size, self.height() - size)
        elif button == self.clear_button:
            button.move(0, self.height() - size)
        elif button == self.rotate_clockwise_button:
            button.move(self.width() - size, 0)
        elif button == self.rotate_counterclockwise_button:
            button.move(0, 0)
