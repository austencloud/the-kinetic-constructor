from typing import TYPE_CHECKING

from PyQt6.QtCore import QEvent, QSize
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGraphicsView, QLabel, QPushButton, QWidget

from utilities.TypeChecking.TypeChecking import LetterDictionary
from utilities.export_handler import ExportHandler
from utilities.json_handler import JsonHandler
from utilities.layout_manager import LayoutManager
from utilities.pictograph_generator import PictographGenerator
from widgets.events.key_event_handler import KeyEventHandler
from widgets.graph_editor import GraphEditor
from widgets.optionboard.optionboard import OptionBoard
from widgets.sequence_board.sequence_board import SequenceBoard

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.propbox.propbox import PropBox


class MainWidget(QWidget):
    propbox: "PropBox"
    main_window: "MainWindow"
    clear_sequence_button: "QPushButton"
    word_label: "QLabel"
    sequence_view: "QGraphicsView"

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window

        self.json_handler = JsonHandler()
        self.letters: LetterDictionary = self.json_handler.load_all_letters()
        self.key_event_handler = KeyEventHandler()
        self.graph_editor = GraphEditor(self)
        self.optionboard = OptionBoard(self)

        self.graphboard = self.graph_editor.graphboard
        self.infobox = self.graph_editor.infobox
        self.propbox = self.graph_editor.propbox
        self.arrowbox = self.graph_editor.arrowbox

        self.sequence_board = SequenceBoard(self, self.graphboard)
        self.generator = PictographGenerator(self, self.graphboard, self.infobox)
        self.export_handler = ExportHandler(self.graphboard)

        self.graphboard.generator = self.generator
        self.sequence_board.generator = self.generator

        self.layout_manager = LayoutManager(self)
        self.layout_manager.configure_layouts()

    ### EVENTS ###

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            self.key_event_handler.keyPressEvent(event, self, self.graphboard)
            return True
        return super().eventFilter(source, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.update_graph_editor_size()
        self.update_optionboard_size()
        self.update_sequenceboard_size()

    def update_graph_editor_size(self) -> None:
        if hasattr(self, "graph_editor"):
            self.graph_editor.setFixedHeight(int(self.height() * 1 / 3))
            self.update_graphboard_size()
            self.update_arrowbox_size()
            self.update_propbox_size()
            self.update_action_button_size()

    def update_graphboard_size(self) -> None:
        graph_editor_height = int(self.height() * 1 / 3)
        if hasattr(self, "graphboard"):
            view_width = int(graph_editor_height * 75 / 90)
            self.graphboard.view.setFixedSize(
                view_width, graph_editor_height
            )
            view_scale = view_width / self.graphboard.width()
            self.graphboard.view.resetTransform()  # Reset the current transform
            self.graphboard.view.scale(view_scale, view_scale)  # Set the new scale
            
    def update_arrowbox_size(self) -> None:
        if hasattr(self, "arrowbox"):
            self.arrowbox.view.setFixedSize(
                int(self.graphboard.view.height() * 1 / 2),
                int(self.graphboard.view.height() * 1 / 2),
            )

    def update_propbox_size(self) -> None:
        if hasattr(self, "propbox"):
            self.propbox.view.setFixedSize(
                int(self.graphboard.view.height() * 1 / 2),
                int(self.graphboard.view.height() * 1 / 2),
            )

    def update_action_button_size(self) -> None:
        if hasattr(self.graph_editor, "action_buttons_frame"):
            button_size = int((self.graph_editor.height() / 6) * 0.8)
            for i in range(
                self.graph_editor.action_buttons_frame.action_buttons_layout.count()
            ):
                button: QPushButton = (
                    self.graph_editor.action_buttons_frame.action_buttons_layout.itemAt(
                        i
                    ).widget()
                )
                button.setFixedSize(button_size, button_size)
                button.setIconSize(
                    QSize(int(button_size * 0.8), int(button_size * 0.8))
                )
            self.graph_editor.action_buttons_frame.setMinimumWidth(button_size)
            self.graph_editor.action_buttons_frame.setMaximumWidth(button_size)

    def update_optionboard_size(self) -> None:
        if hasattr(self, "optionboard"):
            self.optionboard.setFixedHeight(int(self.height() * 2 / 3))
            self.optionboard.update_scroll_area_size()
            self.optionboard.update_letter_buttons_size()
            
       
    def update_sequenceboard_size(self) -> None:
        if hasattr(self, "sequence_board"):
            button_height = int(self.height() * 1/18)
            self.sequence_board.setFixedHeight(int(self.height() - button_height))
