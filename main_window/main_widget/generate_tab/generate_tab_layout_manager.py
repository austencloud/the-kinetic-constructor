from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generate_tab import GenerateTab


class GenerateTabLayoutManager:
    def __init__(self, generate_tab: "GenerateTab"):
        self.generate_tab = generate_tab
        self.top_spacer = None
        self.bottom_spacer = None

    def arrange_layout(self):
        """Organizes the widgets with proper spacing while ensuring full usage of available space."""

        # Top row for the customization label
        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(self.generate_tab.customize_sequence_label)

        # Main content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a spacer above the first widget (Level Selector)
        self.top_spacer = QSpacerItem(
            0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        content_layout.insertSpacerItem(0, self.top_spacer)

        # Add widgets (these should fill space evenly)
        content_layout.addWidget(self.generate_tab.level_selector, 1)
        content_layout.addWidget(self.generate_tab.length_adjuster, 1)
        content_layout.addWidget(self.generate_tab.turn_intensity, 1)
        content_layout.addWidget(self.generate_tab.mode_toggle, 1)
        content_layout.addWidget(self.generate_tab.prop_continuity_toggle, 1)
        content_layout.addWidget(self.generate_tab.letter_picker, 1)
        content_layout.addWidget(self.generate_tab.slice_size_toggle, 1)
        content_layout.addWidget(self.generate_tab.permutation_type, 1)

        # Add a spacer below the last widget, but above the buttons
        self.bottom_spacer = QSpacerItem(
            0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        content_layout.insertSpacerItem(content_layout.count(), self.bottom_spacer)

        # Button row layout
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(int(self.generate_tab.width() * 0.2))
        btn_row.addWidget(self.generate_tab.auto_complete_button)
        btn_row.addWidget(self.generate_tab.generate_button)

        # Add everything to the main layout
        self.generate_tab.main_layout.addLayout(top_row, 1)
        self.generate_tab.main_layout.addLayout(content_layout, 16)
        self.generate_tab.main_layout.addLayout(btn_row, 4)

        self.content_layout = content_layout  # Store content_layout

    def _resize_spacer(self, spacer: QSpacerItem, height: int):
        spacer.changeSize(
            0, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )

    def resize_spacers(self):
        available_height = self.generate_tab.height() // 24
        self._resize_spacer(self.top_spacer, available_height)
        self._resize_spacer(self.bottom_spacer, available_height)
        self.generate_tab.main_layout.update()
