from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generate_tab import GenerateTab


class GenerateTabLayoutManager:
    def __init__(self, parent: "GenerateTab"):
        self.parent = parent

    def arrange_layout(self):
        """Organizes the widgets with proper spacing while ensuring full usage of available space."""

        # Top row for the customization label
        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(self.parent.customize_sequence_label)

        # Main content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a spacer above the first widget (Level Selector)
        self.top_spacer = QSpacerItem(
            0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        content_layout.addSpacerItem(self.top_spacer)

        # Add widgets (these should fill space evenly)
        content_layout.addWidget(self.parent.level_selector, 1)
        content_layout.addWidget(self.parent.length_adjuster, 1)
        content_layout.addWidget(self.parent.turn_intensity, 1)
        content_layout.addWidget(self.parent.mode_toggle, 1)
        content_layout.addWidget(self.parent.rotation_toggle, 1)
        content_layout.addWidget(self.parent.letter_picker, 1)
        content_layout.addWidget(self.parent.rotation_type, 1)

        # Add a spacer below the last widget, but above the buttons
        self.bottom_spacer = QSpacerItem(
            0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        content_layout.addSpacerItem(self.bottom_spacer)

        # Button row layout
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(int(self.parent.width() * 0.2))
        btn_row.addWidget(self.parent.auto_complete_button)
        btn_row.addWidget(self.parent.generate_button)

        # Add everything to the main layout
        self.parent.main_layout.addLayout(top_row)
        self.parent.main_layout.addLayout(content_layout)
        self.parent.main_layout.addLayout(btn_row)
