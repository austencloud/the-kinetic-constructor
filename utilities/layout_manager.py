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
        self.left_layout: QVBoxLayout = self.layouts["right"]
        self.right_layout: QVBoxLayout = self.layouts["left"]
        self.graph_editor_layout: QHBoxLayout = self.layouts["graph_editor"]
        self.objectbox_layout: QVBoxLayout = self.layouts["objectbox"]

        self.graphboard_layout: QVBoxLayout = self.layouts["graphboard"]
        self.word_layout: QHBoxLayout = self.layouts["word"]
        self.graphboard_and_buttons_layout: QHBoxLayout = self.layouts[
            "graphboard_and_buttons"
        ]
        self.letter_buttons_layout: QVBoxLayout = self.layouts["letter_buttons"]
        self.sequence_layout: QVBoxLayout = self.layouts["sequence"]
        self.keyboard_layout: QVBoxLayout = self.layouts["keyboard"]
        self.option_picker_layout: QHBoxLayout = self.layouts["option_picker"]
        self.sequence_layout: QHBoxLayout = self.layouts["sequence"]

        self.option_picker = self.main_widget.option_picker
        self.graph_editor = self.main_widget.graph_editor
        self.sequence = self.main_widget.sequence
        self.graphboard = self.main_widget.graph_editor.graphboard

    def configure_layouts(self) -> None:
        self.configure_main_layout()
        self.init_sequence_layout()
        self.add_black_border_to_widgets()

    def init_layouts(self) -> None:
        self.layouts = {
            "main": QHBoxLayout(),
            "right": QVBoxLayout(),
            "left": QVBoxLayout(),
            "graph_editor": QHBoxLayout(),
            "sequence": QHBoxLayout(),
            "objectbox": QVBoxLayout(),
            "graphboard": QVBoxLayout(),
            "word": QHBoxLayout(),
            "graphboard_and_buttons": QHBoxLayout(),
            "option_picker": QHBoxLayout(),
            "letter_buttons": QVBoxLayout(),
            "sequence": QVBoxLayout(),
            "keyboard": QVBoxLayout(),
        }

    def configure_main_layout(self) -> None:
        self.layouts["left"].addLayout(self.layouts["sequence"])
        self.layouts["right"].addLayout(self.layouts["option_picker"])
        self.layouts["right"].addLayout(self.layouts["graph_editor"])

        self.layouts["main"].addLayout(self.layouts["left"])
        self.layouts["main"].addLayout(self.layouts["right"])

        self.layouts["option_picker"].addWidget(self.main_widget.option_picker)
        self.main_window.graph_editor_layout.addWidget(self.graph_editor)
        self.main_widget.setLayout(self.layouts["main"])
        self.main_widget.layout().setSpacing(0)
        self.main_widget.layout().setContentsMargins(0, 0, 0, 0)

    def init_sequence_layout(self) -> None:
        self.layouts["sequence"].addWidget(self.main_widget.sequence)

    def add_black_border_to_widgets(self) -> None:
        self.add_black_border(self.main_widget.graph_editor.graphboard)
        self.add_black_border(self.main_widget.sequence)
        self.add_black_border(self.main_widget.graph_editor.infobox)
        self.add_black_border(self.main_widget.option_picker)
        self.add_black_border(self.main_widget.option_picker.scroll_area)
        self.add_black_border(self.main_widget.option_picker.button_frame)
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
