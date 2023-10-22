from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class Context_Menu_Manager():
    def __init__(self, parent):
        self.parent = parent
        self.main_widget = self.parent.main_widget

    def create_arrow_menu(self, selected_items, event):
        arrow_menu = QMenu(self.parent)
        self.add_action(arrow_menu, 'Delete', lambda: self.main_widget.arrow_manager.delete_arrow(selected_items))
        self.add_action(arrow_menu, 'Rotate Right', lambda: self.main_widget.arrow_manager.rotate_arrow("right", selected_items))
        self.add_action(arrow_menu, 'Rotate Left', lambda: self.main_widget.arrow_manager.rotate_arrow("left", selected_items))
        self.add_action(arrow_menu, 'Mirror', lambda: self.main_widget.arrow_manager.mirror_arrow(selected_items))
        self.add_action(arrow_menu, 'Bring Forward', lambda: self.main_widget.arrow_manager.bringForward(selected_items))
        arrow_menu.exec_(event.globalPos())

    def create_staff_menu(self, selected_items, event):
        staff_menu = QMenu(self.parent)
        self.add_action(staff_menu, 'Delete', lambda: self.main_widget.arrow_manager.delete_staff(selected_items))
        self.add_action(staff_menu, 'Rotate Right', lambda: self.main_widget.arrow_manager.rotate_arrow("right", selected_items))
        self.add_action(staff_menu, 'Rotate Left', lambda: self.main_widget.arrow_manager.rotate_arrow("left", selected_items))
        staff_menu.exec_(event.globalPos())

    def create_graphboard_menu(self, event):
        graphboard_menu = QMenu(self.parent)
        self.add_action(graphboard_menu, 'Swap Colors', lambda: self.parent.main_widget.arrow_manager.swap_colors(self.parent.get_selected_items()))
        self.add_action(graphboard_menu, 'Select All', self.main_widget.arrow_manager.select_all_arrows)
        self.add_action(graphboard_menu, 'Add to Sequence', lambda _: self.main_widget.sequence_view.add_to_sequence(self.parent))
        self.add_action(graphboard_menu, 'Export to PNG', self.main_widget.graph_editor_widget.export_manager.export_to_png)
        self.add_action(graphboard_menu, 'Export to SVG', self.main_widget.graph_editor_widget.export_manager.export_to_svg)
        graphboard_menu.exec(event.globalPos())

    def add_action(self, menu, label, func):
        action = QAction(label, self.parent)
        action.triggered.connect(func)
        menu.addAction(action)
