from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout


class InfoboxLayouts:
    def __init__(self, infobox, graphboard_view):
        self.infobox = infobox
        self.graphboard_view = infobox.graphboard_view
    
    def define_info_layouts(
        self, motion_type_label, rotation_direction_label, start_end_label, turns_label
    ):
        """Define layouts for the info widget."""
        motion_type_layout = QHBoxLayout()
        motion_type_layout.addWidget(motion_type_label)
        motion_type_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_end_layout = QHBoxLayout()
        start_end_layout.addWidget(start_end_label)
        start_end_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rotation_direction_layout = QHBoxLayout()
        rotation_direction_layout.addWidget(rotation_direction_label)
        rotation_direction_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_layout = QHBoxLayout()
        turns_layout.addWidget(turns_label)
        turns_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(motion_type_layout)
        main_layout.addLayout(start_end_layout)
        main_layout.addLayout(turns_layout)

        return main_layout

    def construct_info_widget(self, attributes, color):
        """Construct a widget displaying arrow information."""
        (
            motion_type_label,
            rotation_direction_label,
            start_end_label,
            turns_label,
        ) = self.create_labels_for_attributes(attributes)

        start_end_layout = QHBoxLayout()
        start_end_button = getattr(self.infobox, f"swap_start_end_{color}_button")
        start_end_layout.addWidget(start_end_button)
        start_end_layout.addWidget(start_end_label)

        # Create the turns layout
        turns_layout = QHBoxLayout()
        decrement_button = getattr(self.infobox, f"decrement_turns_{color}_button")
        increment_button = getattr(self.infobox, f"increment_turns_{color}_button")
        turns_layout.addWidget(decrement_button)
        turns_layout.addWidget(turns_label)
        turns_layout.addWidget(increment_button)

        # Define the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(motion_type_label)
        main_layout.addWidget(rotation_direction_label)
        main_layout.addWidget(start_end_label)
        main_layout.addLayout(turns_layout)  # Add the turns layout here

        info_widget = QWidget()
        info_widget.setLayout(main_layout)
        return info_widget
