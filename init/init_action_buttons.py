#import
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize, Qt
from settings import GRAPHBOARD_SCALE
class Init_Action_Buttons:
    def __init__(self, main_widget, main_window):
        self.init_action_buttons(main_widget, main_window)
        
    def init_action_buttons(self, main_widget, main_window):
        button_font = QFont('Helvetica', 14)
        button_width = 80 * GRAPHBOARD_SCALE
        button_height = 80 * GRAPHBOARD_SCALE
        icon_size = QSize(int(60 * GRAPHBOARD_SCALE), int(60 * GRAPHBOARD_SCALE))
        masterbtnlayout = QVBoxLayout()
        button_layout = QVBoxLayout()

        masterbtnlayout.addLayout(button_layout)

        def createButton(icon_path, tooltip, on_click, is_lambda=False):
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(button_font)
            button.setFixedWidth(int(button_width))
            button.setFixedHeight(int(button_height))
            button.setIconSize(icon_size)
            if is_lambda:
                button.clicked.connect(lambda: on_click())
            else:
                button.clicked.connect(on_click)
            return button

        main_widget.updatePositionButton = createButton("images/icons/update_locations.png", "Update Position", 
            lambda: main_widget.json_manager.update_optimal_locations_in_json(*main_widget.graphboard_view.get_current_arrow_positions()), is_lambda=True)
        main_widget.deleteButton = createButton("images/icons/delete.png", "Delete",
            lambda: main_widget.arrow_manager.delete_arrow(main_widget.graphboard_scene.selectedItems()), is_lambda=True)
        main_widget.rotateRightButton = createButton("images/icons/rotate_right.png", "Rotate Right",
            lambda: main_widget.arrow_manager.rotate_arrow('right', main_widget.graphboard_scene.selectedItems()), is_lambda=True)        
        main_widget.rotateLeftButton = createButton("images/icons/rotate_left.png", "Rotate Left",
            lambda: main_widget.arrow_manager.rotate_arrow('left', main_widget.graphboard_scene.selectedItems()), is_lambda=True)
        main_widget.mirrorButton = createButton("images/icons/mirror.png", "Mirror",
            lambda: main_widget.arrow_manager.mirror_arrow(main_widget.graphboard_scene.selectedItems()), is_lambda=True)
        main_widget.swapColors = createButton("images/icons/swap.png", "Swap Colors",
            lambda: main_widget.arrow_manager.swap_colors(main_widget.graphboard_scene.selectedItems()), is_lambda=True)
        main_widget.selectAllButton = createButton("images/icons/select_all.png", "Select All",
            lambda: main_widget.graphboard_view.select_all_items(), is_lambda=True)
        main_widget.add_to_sequence_button = createButton("images/icons/add_to_sequence.png", "Add to Sequence",
            lambda: main_widget.sequence_manager.add_to_sequence(main_widget.graphboard_view), is_lambda=True)
        
        buttons = [
            main_widget.deleteButton, 
            main_widget.rotateRightButton,
            main_widget.rotateLeftButton,
            main_widget.mirrorButton,
            main_widget.swapColors,
            main_widget.updatePositionButton,
            main_widget.selectAllButton,
            main_widget.add_to_sequence_button
        ]

        for button in buttons:
            button_layout.addWidget(button)

        main_window.button_layout.addLayout(masterbtnlayout)