from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QLineEdit, QLabel, QTextEdit

if TYPE_CHECKING:
    from widgets.graph_editor.infobox.infobox import InfoBox
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
from widgets.graph_editor.infobox.attribute_panel.attribute_box import AttributeBox
from widgets.graph_editor.infobox.infobox_frames import InfoBoxFrames


class InfoPanel(QFrame):
    def __init__(self, infobox: "InfoBox", graphboard: "GraphBoard") -> None:
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

    def update_info_panel(self) -> None:
        pass
        # self.update_letter_line()
        # self.update_letter_type_line()
        # self.update_motion_line()
        # self.update_additional_info()

    def update_type_and_position_label(self) -> None:
        """
        Update the type and position label based on the current letter and its type.
        """
        (
            current_letter,
            current_letter_type,
        ) = (
            self.graphboard.current_letter,
            self.graphboard.get_current_letter_type(),
        )
        if current_letter and current_letter_type:
            start_end_positions = self.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            self.type_position_label.setText("")
