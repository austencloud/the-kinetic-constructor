from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QPoint
from settings.string_constants import RIGHT, LEFT
from objects.arrow import Arrow
from objects.staff import Staff

from typing import TYPE_CHECKING, List, Tuple, Callable
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graphboard.graphboard import GraphBoard


class GraphBoardMenuHandler:
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        self.graphboard = graphboard
        self.main_widget = main_widget
        self.export_handler = main_widget.export_handler

    def create_menu_with_actions(self, actions: List[Tuple[str, Callable]], event_pos: QPoint) -> None:
        menu = QMenu()
        for label, func in actions:
            action = QAction(label, self.graphboard)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec(event_pos)

    def create_arrow_menu(self, selected_item, event) -> None:
        selected_arrow = selected_item if isinstance(selected_item, Arrow) else None

        actions = [
            ("Delete", lambda: selected_arrow.delete()),
            (
                "Rotate Right",
                lambda: selected_arrow.rotate(RIGHT),
            ),
            (
                "Rotate Left",
                lambda: selected_arrow.rotate(LEFT),
            ),
            ("Mirror", lambda: selected_arrow.mirror()),
            ("Increment Turns", lambda: selected_arrow.increment_turns()),
            ("Decrement Turns", lambda: selected_arrow.decrement_turns()),
            
        ]
        self.create_menu_with_actions(actions, event)

    def create_staff_menu(self, selected_item, event) -> None:
        selected_staff = selected_item if isinstance(selected_item, Staff) else None

        actions = [
            ("Delete", lambda: selected_staff.delete()),
            (
                "Swap Axis",
                lambda: selected_staff.swap_axis(),
            ),
        ]
        self.create_menu_with_actions(actions, event)

    def create_graphboard_menu(self, event) -> None:
        actions = [
            ("Swap Colors", lambda: self.manipulators.swap_colors()),
            (
                "Add to Sequence",
                lambda _: self.graphboard.add_to_sequence(
                    self.graphboard
                ),  # Need to implement this method
            ),
            ("Export to PNG", self.export_handler.export_to_png),
            ("Export to SVG", lambda: self.export_handler.export_to_svg("output.svg")),
        ]
        self.create_menu_with_actions(actions, event)
