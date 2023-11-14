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

    def configure_layouts(self) -> None:
        self.configure_main_layout()
        self.init_sequence_layout()
        # Un-comment this for layout testing
        # self.add_black_border_to_widgets() 

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
            "sequence_with_label_and_button": QVBoxLayout(),
            "keyboard": QVBoxLayout(),
        }

    def configure_main_layout(self) -> None:
        self.layouts["left"].addLayout(self.layouts["sequence"])
        self.layouts["left"].addLayout(self.layouts["graph_editor"])
        self.layouts["main"].addLayout(self.layouts["left"])
        self.layouts["right"].addLayout(self.layouts["optionboard"])
        self.layouts["main"].addLayout(self.layouts["right"])
        self.layouts["optionboard"].addWidget(self.main_widget.optionboard.view)
        self.main_widget.setLayout(self.layouts["main"])

    def init_sequence_layout(self) -> None:
        self.layouts["sequence_with_label_and_button"].addWidget(
            self.main_widget.word_label
        )
        self.layouts["sequence_with_label_and_button"].addWidget(
            self.main_widget.sequence_board.view
        )
        self.layouts["sequence_with_label_and_button"].addWidget(
            self.main_widget.clear_sequence_button
        )
        self.layouts["sequence"].addLayout(
            self.layouts["sequence_with_label_and_button"]
        )

    def add_black_border_to_widgets(self) -> None:
        self.add_black_border(self.main_widget.graph_editor.graphboard)
        self.add_black_border(self.main_widget.sequence_board)
        self.add_black_border(self.main_widget.word_label)
        self.add_black_border(self.main_widget.graph_editor.infobox)
        self.add_black_border(self.main_widget.optionboard.view)
        self.add_black_border(self.main_widget.graph_editor.action_buttons_frame)
        self.add_black_border(self.main_widget.letter_buttons_frame)
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
        else:
            print(f"Widget {widget} is not a QFrame and does not support setFrameStyle.")