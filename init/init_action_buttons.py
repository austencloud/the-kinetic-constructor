#import
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt

class Init_Action_Buttons:
    def __init__(self, ui_setup, main_window):
        self.init_action_buttons(ui_setup, main_window)
        
    def init_action_buttons(self, ui_setup, main_window):
        button_font = QFont('Helvetica', 14)
        button_width = 60
        button_height = 60
        icon_size = QSize(40, 40)
        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QHBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        def createButton(icon_path, tooltip, on_click, is_lambda=False):
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(button_font)
            button.setFixedWidth(button_width)
            button.setFixedHeight(button_height)
            button.setIconSize(icon_size)
            if is_lambda:
                button.clicked.connect(lambda: on_click())
            else:
                button.clicked.connect(on_click)
            return button

        ui_setup.updatePositionButton = createButton("images/icons/update_locations.png", "Update Position", 
            lambda: ui_setup.json_manager.update_optimal_locations_in_json(*ui_setup.graphboard_view.get_current_arrow_positions()), is_lambda=True)
        ui_setup.deleteButton = createButton("images/icons/delete.png", "Delete",
            lambda: ui_setup.arrow_manager.delete_arrow(ui_setup.graphboard_scene.selectedItems()), is_lambda=True)
        ui_setup.rotateRightButton = createButton("images/icons/rotate_right.png", "Rotate Right",
            lambda: ui_setup.arrow_manager.rotate_arrow('right', ui_setup.graphboard_scene.selectedItems()), is_lambda=True)        
        ui_setup.rotateLeftButton = createButton("images/icons/rotate_left.png", "Rotate Left",
            lambda: ui_setup.arrow_manager.rotate_arrow('left', ui_setup.graphboard_scene.selectedItems()), is_lambda=True)
        ui_setup.mirrorButton = createButton("images/icons/mirror.png", "Mirror",
            lambda: ui_setup.arrow_manager.mirror_arrow(ui_setup.graphboard_scene.selectedItems()), is_lambda=True)
        ui_setup.swapColors = createButton("images/icons/swap.png", "Swap Colors",
            lambda: ui_setup.arrow_manager.swap_colors(ui_setup.graphboard_scene.selectedItems()), is_lambda=True)
        ui_setup.selectAllButton = createButton("images/icons/select_all.png", "Select All",
            lambda: ui_setup.graphboard_view.select_all_items(), is_lambda=True)
        ui_setup.add_to_sequence_button = createButton("images/icons/add_to_sequence.png", "Add to Sequence",
            lambda: ui_setup.sequence_manager.add_to_sequence(ui_setup.graphboard_view), is_lambda=True)
        
        buttons = [
            ui_setup.deleteButton, 
            ui_setup.rotateRightButton,
            ui_setup.rotateLeftButton,
            ui_setup.mirrorButton,
            ui_setup.swapColors,
            ui_setup.updatePositionButton,
            ui_setup.selectAllButton,
            ui_setup.add_to_sequence_button
        ]

        for button in buttons:
            buttonstack.addWidget(button)

        main_window.button_layout.addLayout(masterbtnlayout)