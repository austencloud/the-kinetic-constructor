from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from settings.string_constants import *


class GraphboardContextMenuHandler:
    def __init__(self, scene):
        self.main_widget = scene.main_widget
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator
        self.arrow_selector = self.arrow_manager.selector
        self.export_manager = scene.export_manager
        self.staff_handler = scene.staff_handler
        self.staff_visibility_manager = self.staff_handler.visibility_manager
        self.sequence_view = self.main_widget.sequence_view

    def create_menu_with_actions(self, parent, actions, event):
        menu = QMenu(parent)
        for label, func in actions:
            action = QAction(label, parent)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec(event.globalPos())

    def create_arrow_menu(self, selected_items, event):
        actions = [
            ("Delete", lambda: self.arrow_selector.delete_arrow(selected_items)),
            (
                "Rotate Right",
                lambda: self.arrow_manipulator.rotate_arrow(RIGHT, selected_items),
            ),
            (
                "Rotate Left",
                lambda: self.arrow_manipulator.rotate_arrow(LEFT, selected_items),
            ),
            ("Mirror", lambda: self.arrow_manipulator.mirror_arrow(selected_items)),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)

    def create_staff_menu(self, selected_items, event):
        actions = [
            ("Delete", lambda: self.staff_selector.delete_staff(selected_items)),
            (
                "Rotate Right",
                lambda: self.arrow_manipulator.rotate_arrow(RIGHT, selected_items),
            ),
            (
                "Rotate Left",
                lambda: self.arrow_manipulator.rotate_arrow(LEFT, selected_items),
            ),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)

    def create_graphboard_menu(self, event):
        actions = [
            ("Swap Colors", lambda: self.arrow_manipulator.swap_colors()),
            ("Select All", self.graphboard.select_all_arrows),
            (
                "Add to Sequence",
                lambda _: self.sequence_view.add_to_sequence(self.graphboard),
            ),
            ("Export to PNG", self.export_manager.export_to_png),
            ("Export to SVG", lambda: self.export_manager.export_to_svg("output.svg")),
        ]
        self.create_menu_with_actions(self.graphboard, actions, event)
