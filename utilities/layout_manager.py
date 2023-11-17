from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGraphicsView,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtGui import QPalette, QColor
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class LayoutManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.layouts: Dict[str, QHBoxLayout | QVBoxLayout] = {}
        self.init_layouts()
        self.assign_layouts_to_window()
        self.main_layout: QHBoxLayout = self.layouts["main"]
        self.left_layout: QVBoxLayout = self.layouts["left"]
        self.right_layout: QVBoxLayout = self.layouts["right"]
        self.graph_editor_layout: QHBoxLayout = self.layouts["graph_editor"]
        self.objectbox_layout: QVBoxLayout = self.layouts["objectbox"]

        self.graphboard_layout: QVBoxLayout = self.layouts["graphboard"]
        self.word_layout: QHBoxLayout = self.layouts["word"]
        self.graphboard_and_buttons_layout: QHBoxLayout = self.layouts[
            "graphboard_and_buttons"
        ]
        self.letter_buttons_layout: QVBoxLayout = self.layouts["letter_buttons"]
        self.sequence_board_layout: QVBoxLayout = self.layouts["sequence_board"]
        self.keyboard_layout: QVBoxLayout = self.layouts["keyboard"]
        self.optionboard_layout: QHBoxLayout = self.layouts["optionboard"]
        self.sequence_layout: QHBoxLayout = self.layouts["sequence"]

        self.optionboard = self.main_widget.optionboard
        self.graph_editor = self.main_widget.graph_editor
        self.sequence_board = self.main_widget.sequence_board
        self.graphboard = self.main_widget.graph_editor.graphboard

    def configure_layouts(self) -> None:
        self.configure_main_layout()
        self.init_sequence_layout()
        self.remove_padding()
        self.add_stretch()
        self.set_contents_margins_to_zero()
        self.add_black_border_to_widgets()

    def remove_padding(self):
        self.layouts["optionboard"].setSpacing(0)
        self.layouts["graph_editor"].setSpacing(0)  # Toggle this for layout testing

    def init_layouts(self) -> None:
        self.layouts = {
            "main": QHBoxLayout(),
            "left": QVBoxLayout(),
            "right": QVBoxLayout(),
            "graph_editor": QHBoxLayout(),
            "sequence": QHBoxLayout(),
            "objectbox": QVBoxLayout(),
            "graphboard": QVBoxLayout(),
            "word": QHBoxLayout(),
            "graphboard_and_buttons": QHBoxLayout(),
            "optionboard": QHBoxLayout(),
            "letter_buttons": QVBoxLayout(),
            "sequence_board": QVBoxLayout(),
            "keyboard": QVBoxLayout(),
        }

    def configure_main_layout(self) -> None:
        self.layouts["left"].addLayout(self.layouts["optionboard"])
        self.layouts["left"].addLayout(self.layouts["graph_editor"])
        self.layouts["main"].addLayout(self.layouts["left"])
        self.layouts["right"].addLayout(self.layouts["sequence"])
        self.layouts["main"].addLayout(self.layouts["right"])
        self.layouts["optionboard"].addWidget(self.main_widget.optionboard)
        self.main_widget.setLayout(self.layouts["main"])
        self.main_window.graph_editor_layout.addWidget(
            self.graph_editor
        )

    def add_stretch(self) -> None:
        self.main_window.graph_editor_layout.addStretch(1)
        self.main_window.optionboard_layout.addStretch(1)

    def set_contents_margins_to_zero(self) -> None:
        self.graph_editor.graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.optionboard_layout.setContentsMargins(0, 0, 0, 0)
        self.optionboard.optionboard_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def init_sequence_layout(self) -> None:
        self.layouts["sequence_board"].addWidget(self.main_widget.sequence_board)
        self.layouts["sequence_board"].addWidget(self.main_widget.clear_sequence_button)
        self.layouts["sequence"].addLayout(self.layouts["sequence_board"])

    def add_black_border_to_widgets(self) -> None:
        self.add_black_border(self.main_widget.graph_editor.graphboard)
        self.add_black_border(self.main_widget.sequence_board)
        self.add_black_border(self.main_widget.graph_editor.infobox)
        self.add_black_border(self.main_widget.optionboard)
        self.add_black_border(self.main_widget.graph_editor.action_buttons_frame)
        self.add_black_border(self.main_widget.graph_editor.graphboard)
        self.add_black_border(self.main_widget.graph_editor.propbox)

    def assign_layouts_to_window(self) -> None:
        for layout_name, layout in self.layouts.items():
            setattr(self.main_window, f"{layout_name}_layout", layout)

    def add_black_border(
        self, widget: QWidget | QGraphicsView | QLabel | QPushButton | QFrame
    ) -> None:
        if isinstance(widget, QFrame):
            try:
                widget.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                widget.setLineWidth(1)
                palette = widget.palette()
                palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
                widget.setPalette(palette)
            except AttributeError:
                print(f"Widget {widget} does not have a setFrameStyle method.")
