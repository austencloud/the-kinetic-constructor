from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QLineEdit, QLabel, QTextEdit
if TYPE_CHECKING:
    from widgets.graph_editor.infobox.infobox import InfoBox
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
from widgets.graph_editor.infobox.infobox_labels import InfoBoxLabels
from widgets.graph_editor.infobox.infobox_frames import InfoBoxFrames

class InfoPanel(QFrame):
    def __init__(self, infobox: 'InfoBox', graphboard: 'GraphBoard') -> None:
        super().__init__()
        self.infobox = infobox
        self.graphboard = graphboard
        self.setup_info_panel()

    def setup_info_panel(self) -> None:
        # Create the vbox layout
        layout = QVBoxLayout(self)

        # Create the top box
        top_box = QGroupBox("Top Box")
        top_layout = QVBoxLayout(top_box)

        # Add lines for letter and letter type
        letter_line = QLineEdit()
        letter_type_line = QLineEdit()
        top_layout.addWidget(QLabel("Letter:"))
        top_layout.addWidget(letter_line)
        top_layout.addWidget(QLabel("Type:"))
        top_layout.addWidget(letter_type_line)

        # Add motion to motion indication line
        motion_line = QLineEdit()
        top_layout.addWidget(QLabel("Motion to motion indication:"))
        top_layout.addWidget(motion_line)

        # Add the top box to the layout
        layout.addWidget(top_box)

        # Create the bottom box
        bottom_box = QGroupBox("Bottom Box")
        bottom_layout = QVBoxLayout(bottom_box)

        # Add additional information
        additional_info = QTextEdit()
        bottom_layout.addWidget(QLabel("Additional Information:"))
        bottom_layout.addWidget(additional_info)

        # Add the bottom box to the layout
        layout.addWidget(bottom_box)

        # Set the layout for the info panel
        self.setLayout(layout)
    