from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class GraphboardContextMenuHandler():
    def __init__(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.main_widget = self.graphboard_view.main_widget
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.arrow_manipulator
        self.arrow_selector = self.arrow_manager.arrow_selector
        self.export_manager = self.graphboard_view.export_manager


    def create_menu_with_actions(self, parent, actions, event):
        menu = QMenu(parent)
        for label, func in actions:
            action = QAction(label, parent)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec(event.globalPos())

    def create_arrow_menu(self, selected_items, event):
        actions = [
            ('Delete', lambda: self.arrow_selector.delete_arrow(selected_items)),
            ('Rotate Right', lambda: self.arrow_manipulator.rotate_arrow("right", selected_items)),
            ('Rotate Left', lambda: self.arrow_manipulator.rotate_arrow("left", selected_items)),
            ('Mirror', lambda: self.arrow_manipulator.mirror_arrow(selected_items))
        ]
        self.create_menu_with_actions(self.graphboard_view, actions, event)

    def create_staff_menu(self, selected_items, event):
        actions = [
            ('Delete', lambda: self.arrow_selector.delete_staff(selected_items)),
            ('Rotate Right', lambda: self.arrow_manipulator.rotate_arrow("right", selected_items)),
            ('Rotate Left', lambda: self.arrow_manipulator.rotate_arrow("left", selected_items))
        ]
        self.create_menu_with_actions(self.graphboard_view, actions, event)

    def create_graphboard_menu(self, event):
        actions = [
            ('Swap Colors', lambda: self.arrow_manipulator.swap_colors(self.graphboard_view.get_selected_items())),
            ('Select All', self.graphboard_view.select_all_arrows),
            ('Add to Sequence', lambda _: self.sequence_view.add_to_sequence(self.graphboard_view)),
            ('Export to PNG', self.export_manager.export_to_png),
            ('Export to SVG', self.export_manager.export_to_svg)
        ]
        self.create_menu_with_actions(self.graphboard_view, actions, event)
