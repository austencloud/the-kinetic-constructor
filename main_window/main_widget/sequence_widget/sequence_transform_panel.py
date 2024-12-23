from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget

from utilities.path_helpers import get_images_and_data_path


class SequenceTransformPanel(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.colors_swapped = False
        # Create a horizontal layout
        layout = QHBoxLayout(self)
        # center contents
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Mirror button
        self.mirror_button = QPushButton()
        mirror_icon = get_images_and_data_path(
            "images/icons/sequence_widget_icons/mirror.png"
        )
        self.mirror_button.setIcon(QIcon(mirror_icon))
        self.mirror_button.setToolTip("Mirror Sequence")
        self.mirror_button.clicked.connect(
            self.sequence_widget.mirror_manager.mirror_current_sequence
        )
        layout.addWidget(self.mirror_button)

        # Swap colors button
        self.swap_colors_button = QPushButton()
        swap_icon = get_images_and_data_path(
            "images/icons/sequence_widget_icons/yinyang1.png"
        )
        self.swap_colors_button.setIcon(QIcon(swap_icon))
        self.swap_colors_button.setToolTip("Swap Colors")
        self.swap_colors_button.clicked.connect(
            self.sequence_widget.color_swap_manager.swap_colors_in_sequence
        )
        layout.addWidget(self.swap_colors_button)

        # Rotate button
        self.rotate_button = QPushButton()
        rotate_icon = get_images_and_data_path(
            "images/icons/sequence_widget_icons/rotate.png"
        )
        self.rotate_button.setIcon(QIcon(rotate_icon))
        self.rotate_button.setToolTip("Rotate Sequence")
        self.rotate_button.clicked.connect(
            self.sequence_widget.rotation_manager.rotate_beats
        )
        layout.addWidget(self.rotate_button)

    def resizeEvent(self, event):
        button_size = self.sequence_widget.width() // 18
        self.mirror_button.setMaximumSize(button_size, button_size)
        self.swap_colors_button.setMaximumSize(button_size, button_size)
        self.rotate_button.setMaximumSize(button_size, button_size)

        icon_size = int(button_size * 0.9)
        icon_size = QSize(icon_size, icon_size)
        self.mirror_button.setIconSize(icon_size)
        self.swap_colors_button.setIconSize(icon_size)
        self.rotate_button.setIconSize(icon_size)

        super().resizeEvent(event)

    def toggle_swap_colors_icon(self):
        if self.colors_swapped:
            new_icon_path = get_images_and_data_path(
                "images/icons/sequence_widget_icons/yinyang1.png"
            )
            self.colors_swapped = False
        else:
            new_icon_path = get_images_and_data_path(
                "images/icons/sequence_widget_icons/yinyang2.png"
            )
            self.colors_swapped = True
        new_icon = QIcon(new_icon_path)
        self.swap_colors_button.setIcon(new_icon)
        QApplication.processEvents()
