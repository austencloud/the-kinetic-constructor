from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from config.string_constants import *


class GraphboardContextMenuHandler:
    def __init__(self, graphboard):
        self.main_widget = graphboard.main_widget
        self.export_manager = graphboard.export_manager
        self.sequence_view = self.main_widget.sequence_view
        self.graphboard = graphboard
        self.manipulators = graphboard.manipulators

    def create_menu_with_actions(self, parent, actions, event_pos):
        menu = QMenu()
        for label, func in actions:
            action = QAction(label, parent)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec(event_pos)

    def create_arrow_menu(self, selected_items, event):
        actions = [
            ("Delete", lambda: self.graphboard.delete_arrow(selected_items)),
            (
                "Rotate Right",
                lambda: self.manipulators.rotate_arrow(RIGHT, selected_items),
            ),
            (
                "Rotate Left",
                lambda: self.manipulators.rotate_arrow(LEFT, selected_items),
            ),
            ("Mirror", lambda: self.manipulators.mirror_arrow(selected_items)),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)

    def create_staff_menu(self, selected_items, event):
        actions = [
            ("Delete", lambda: self.graphboard.delete_staff(selected_items)),
            (
                "Rotate Right",
                lambda: self.manipulators.rotate_arrow(RIGHT, selected_items),
            ),
            (
                "Rotate Left",
                lambda: self.manipulators.rotate_arrow(LEFT, selected_items),
            ),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)

    def create_graphboard_menu(self, event):
        actions = [
            ("Swap Colors", lambda: self.manipulators.swap_colors()),
            ("Select All", self.graphboard.select_all_arrows),
            (
                "Add to Sequence",
                lambda _: self.sequence_view.add_to_sequence(self.graphboard),
            ),
            ("Export to PNG", self.export_manager.export_to_png),
            ("Export to SVG", lambda: self.export_manager.export_to_svg("output.svg")),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)
