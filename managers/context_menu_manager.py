from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class GraphboardContextMenuManager():
    def __init__(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.main_widget = self.graphboard_view.main_widget
        self.arrow_manager = self.main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.arrow_manipulator
        self.arrow_selector = self.arrow_manager.arrow_selector
        self.export_manager = self.graphboard_view.export_manager


    def create_arrow_menu(self, selected_items, event):
        arrow_menu = QMenu(self.parent)
        self.add_action(arrow_menu, 'Delete', lambda: self.arrow_selector.delete_arrow(selected_items))
        self.add_action(arrow_menu, 'Rotate Right', lambda: self.arrow_manipulator.rotate_arrow("right", selected_items))
        self.add_action(arrow_menu, 'Rotate Left', lambda: self.arrow_manipulator.rotate_arrow("left", selected_items))
        self.add_action(arrow_menu, 'Mirror', lambda: self.arrow_manipulator.mirror_arrow(selected_items))
        arrow_menu.exec_(event.globalPos())

    def create_staff_menu(self, selected_items, event):
        staff_menu = QMenu(self.parent)
        self.add_action(staff_menu, 'Delete', lambda: self.arrow_selector.delete_staff(selected_items))
        self.add_action(staff_menu, 'Rotate Right', lambda: self.arrow_manipulator.rotate_arrow("right", selected_items))
        self.add_action(staff_menu, 'Rotate Left', lambda: self.arrow_manipulator.rotate_arrow("left", selected_items))
        staff_menu.exec_(event.globalPos())

    def create_graphboard_menu(self, event):
        graphboard_menu = QMenu(self.graphboard_view)
        self.add_action(graphboard_menu, 'Swap Colors', lambda: self.arrow_manipulator.swap_colors(self.graphboard_view.get_selected_items()))
        self.add_action(graphboard_menu, 'Select All', self.arrow_manager.select_all_arrows)
        self.add_action(graphboard_menu, 'Add to Sequence', lambda _: self.sequence_view.add_to_sequence(self.graphboard_view))
        self.add_action(graphboard_menu, 'Export to PNG', self.export_manager.export_to_png)
        self.add_action(graphboard_menu, 'Export to SVG', self.export_manager.export_to_svg)
        graphboard_menu.exec(event.globalPos())

    def add_action(self, menu, label, func):
        action = QAction(label, self.graphboard_view)
        action.triggered.connect(func)
        menu.addAction(action)
