from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize
from resources.constants import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QVBoxLayout
from objects.arrow.arrow import Arrow

class ActionButtonsFrame(QFrame):
    def __init__(self, graphboard_view, json_handler, arrow_manipulator, arrow_selector, sequence_view):
        super().__init__()
        self.graphboard_view = graphboard_view
        self.graphboard_scene = graphboard_view.scene()
        self.json_handler = json_handler
        self.arrow_manipulator = arrow_manipulator
        self.arrow_selector = arrow_selector
        self.sequence_view = sequence_view
        button_font = QFont('Helvetica', 14)
        button_size = int(100 * GRAPHBOARD_SCALE)
        icon_size = QSize(int(80 * GRAPHBOARD_SCALE), int(70 * GRAPHBOARD_SCALE))
        self.action_buttons_layout = QVBoxLayout()
        self.action_buttons_layout.setSpacing(3)
        icons_path = "resources/images/icons/"
        
        # Configuration for each button
        buttons_config = [
            (icons_path + "update_locations.png", "Update Position", 
             lambda: self.json_handler.update_optimal_locations_in_json(*self.graphboard_view.get_current_arrow_positions())),
            (icons_path + "delete.png", "Delete", 
             lambda: self.arrow_selector.delete_arrow(self.graphboard_scene.selectedItems())),
            (icons_path + "rotate_right.png", "Rotate Right",
             lambda: self.arrow_manipulator.rotate_arrow('right', self.graphboard_scene.selectedItems())),
            (icons_path + "rotate_left.png", "Rotate Left",
                lambda: self.arrow_manipulator.rotate_arrow('left', self.graphboard_scene.selectedItems())),
            (icons_path + "mirror.png", "Mirror",
                lambda: self.arrow_manipulator.mirror_arrow(self.graphboard_scene.selectedItems(), self.get_selected_arrow_color())),
            (icons_path + "swap.png", "Swap Colors",
                lambda: self.arrow_manipulator.swap_colors()),
            (icons_path + "select_all.png", "Select All",
                lambda: self.graphboard_view.select_all_items()),
            (icons_path + "add_to_sequence.png", "Add to Sequence",
                lambda: self.sequence_view.add_to_sequence(self.graphboard_view))
        ]
            
        # Function to create a configured button
        def create_configured_button(icon_path, tooltip, on_click):
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(button_font)
            button.setFixedSize(button_size, button_size)
            button.setIconSize(icon_size)
            button.clicked.connect(on_click)
            return button

        # Create and add buttons to the layout
        for icon, tooltip, action in buttons_config:
            button = create_configured_button(icon, tooltip, action)
            self.action_buttons_layout.addWidget(button)
            
        self.setLayout(self.action_buttons_layout)

    def get_selected_arrow_color(self):
        selected_items = self.main_widget.graphboard_scene.selectedItems()
        if selected_items and isinstance(selected_items[0], Arrow):
            return selected_items[0].color
        return None
