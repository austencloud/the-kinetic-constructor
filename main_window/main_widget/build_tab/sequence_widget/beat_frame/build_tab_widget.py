from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.build_tab.sequence_widget.sequence_widget import (
        SequenceWidget,
    )
    from main_window.main_widget.build_tab.option_picker.manual_builder import (
        ManualBuilder,
    )


class BuildTabWidget(QWidget):
    def __init__(
        self, sequence_widget: "SequenceWidget", manual_builder: "ManualBuilder"
    ):
        super().__init__()
        self.sequence_widget = sequence_widget
        self.manual_builder = manual_builder

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.manual_builder)

        # Set stretch factors to give equal space
        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 1)

        # Ensure widgets expand
        self.sequence_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.manual_builder.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
