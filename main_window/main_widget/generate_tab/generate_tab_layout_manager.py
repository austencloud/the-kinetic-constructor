from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generate_tab import GenerateTab


class GenerateTabLayoutManager:
    def __init__(self, parent: "GenerateTab"):
        self.parent = parent
        self.top_spacer: QSpacerItem = QSpacerItem(0, 0)
        self.bottom_spacer: QSpacerItem = QSpacerItem(0, 0)

    def arrange_layout(self):
        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(self.parent.customize_sequence_label)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(self.parent.level_selector, 1)
        content_layout.addWidget(self.parent.length_adjuster, 1)
        content_layout.addWidget(self.parent.turn_intensity, 1)
        content_layout.addWidget(self.parent.mode_toggle, 1)
        content_layout.addWidget(self.parent.rotation_toggle, 1)
        content_layout.addWidget(self.parent.letter_picker, 1)
        content_layout.addWidget(self.parent.rotation_type, 1)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(int(self.parent.width() * 0.2))
        btn_row.addWidget(self.parent.auto_complete_button)
        btn_row.addWidget(self.parent.generate_button)

        self.parent.main_layout.addLayout(top_row)
        self.parent.main_layout.addSpacerItem(self.top_spacer)
        self.parent.main_layout.addLayout(content_layout)
        self.parent.main_layout.addSpacerItem(self.bottom_spacer)
        self.parent.main_layout.addLayout(btn_row)

    def resizeEvent(self, event):
        spacer_height = self.parent.height() * 0.1
        self.top_spacer.changeSize(0, spacer_height)
        self.bottom_spacer.changeSize(0, spacer_height)
