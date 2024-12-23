from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.build_tab.sequence_widget.sequence_widget import (
        SequenceWidget,
    )
    from main_window.main_widget.build_tab.sequence_generator.sequence_generator_widget import (
        SequenceGeneratorWidget,
    )


class GenerateTabWidget(QWidget):
    def __init__(
        self,
        sequence_widget: "SequenceWidget",
        sequence_generator: "SequenceGeneratorWidget",
    ):
        super().__init__()
        self.sequence_widget = sequence_widget
        self.sequence_generator = sequence_generator

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.sequence_generator)

        # Set stretch factors to give equal space
        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 1)

        # Ensure widgets expand
        self.sequence_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.sequence_generator.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
