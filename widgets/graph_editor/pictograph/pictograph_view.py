from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from settings.string_constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
from PyQt6.QtCore import QSize


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None

        # Initialize buttons
        self.init_buttons()

        # Update pictograph size
        self.update_pictograph_size()

    def remove_buttons(self) -> None:
        self.add_to_sequence_button.deleteLater()
        self.clear_button.deleteLater()
        self.rotate_cw_button.deleteLater()
        self.rotate_ccw_button.deleteLater()

    def init_buttons(self) -> None:
        self.add_to_sequence_button = self.create_button(
            f"{ICON_DIR}add_to_sequence.png",
            self.pictograph.add_to_sequence_callback,
        )
        self.clear_button = self.create_button(
            f"{ICON_DIR}clear.png", self.pictograph.clear_pictograph
        )
        self.rotate_cw_button = self.create_button(
            f"{ICON_DIR}rotate_cw.png",
            lambda: self.pictograph.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_ccw_button = self.create_button(
            f"{ICON_DIR}rotate_ccw.png",
            lambda: self.pictograph.rotate_pictograph(COUNTER_CLOCKWISE),
        )

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def configure_button_size_and_position(self, button: QPushButton, size) -> None:
        button.setFixedSize(size, size)
        icon_size = int(size * 0.8)
        button.setIconSize(QSize(icon_size, icon_size))

        # Custom positioning logic if needed
        if button == self.add_to_sequence_button:
            button.move(self.width() - size, self.height() - size)
        elif button == self.clear_button:
            button.move(0, self.height() - size)
        elif button == self.rotate_cw_button:
            button.move(self.width() - size, 0)
        elif button == self.rotate_ccw_button:
            button.move(0, 0)

    def update_pictograph_size(self) -> None:
        # Calculate the view height based on the GraphEditor's height
        view_height = int(self.pictograph.graph_editor.height())
        # Calculate the view width maintaining the aspect ratio (75/90)
        view_width = int(view_height * 75 / 90)

        # Set the size of the view
        self.setMinimumSize(view_width, view_height)
        self.setMaximumSize(view_width, view_height)

        # Calculate the scaling factor
        self.view_scale = min(
            view_width / self.pictograph.sceneRect().width(),
            view_height / self.pictograph.sceneRect().height(),
        )

        # Reset any existing transformations and apply the new scale
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

        # Update the size and position of the buttons
        button_size = int(view_width / 7)
        self.configure_button_size_and_position(
            self.add_to_sequence_button, button_size
        )
        self.configure_button_size_and_position(self.clear_button, button_size)
        self.configure_button_size_and_position(self.rotate_cw_button, button_size)
        self.configure_button_size_and_position(self.rotate_ccw_button, button_size)
