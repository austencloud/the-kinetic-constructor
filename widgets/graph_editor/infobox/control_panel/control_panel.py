from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from settings.string_constants import RED, BLUE
from widgets.graph_editor.infobox.infobox_labels import InfoBoxLabels
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.infobox import InfoBox

class ControlPanel(QFrame):
    def __init__(self, infobox: 'InfoBox', graphboard: 'GraphBoard') -> None:
        super().__init__()
        self.infobox = infobox
        self.graphboard = graphboard
        self.labels = InfoBoxLabels(self, graphboard)
        
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.control_panel_layout = QVBoxLayout(self)

        self.setup_column_layout(BLUE)
        self.setup_column_layout(RED)

        infobox_width = self.infobox.width()
        control_panel_min_width = int(infobox_width * 0.5)
        self.setMinimumWidth(control_panel_min_width)
            
    def setup_column_layout(self, color) -> None:
        column_frame = QFrame()
        column_frame.setFrameShape(QFrame.Shape.Box)
        column_frame.setFrameShadow(QFrame.Shadow.Sunken)
        column_frame.setStyleSheet("border: 1px solid black;")

        column_layout = QVBoxLayout(column_frame)
        column_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to hug the top
        column_layout.setSpacing(0)  # Remove spacing if you want labels closer to each other

        header_label: QLabel = getattr(self.labels, f"{color.lower()}_details_label")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addWidget(header_label)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        column_layout.addLayout(header_layout)
        column_layout.addStretch()  # Add stretch to push the label to the top

        self.control_panel_layout.addWidget(column_frame)


    def update_control_panel(self) -> None:
        # Get the arrow objects from the graphboard
        blue_arrow = self.graphboard.get_arrow_by_color(BLUE)
        red_arrow = self.graphboard.get_arrow_by_color(RED)

        # Update the display for each arrow if it exists
        if blue_arrow:
            self.labels.update_labels(self.labels.blue_details_label.parentWidget(), blue_arrow)
        if red_arrow:
            self.labels.update_labels(self.labels.red_details_label.parentWidget(), red_arrow)