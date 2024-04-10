from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QFrame,
    QVBoxLayout,
)

from path_helpers import get_my_photos_path


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetButton(QPushButton):
    def __init__(self, icon_path: str):
        super().__init__()
        self.setIcon(QIcon(icon_path))

    def enterEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)


class SequenceWidgetButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.orientations = ["in", "counter", "out", "clock"]
        self.font_size = self.sequence_widget.width() // 45

        self._setup_dependencies()
        self._setup_buttons()
        self._setup_layout()

    def _setup_dependencies(self):
        self.main_widget = self.sequence_widget.main_widget
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.builder_toolbar = self.sequence_widget.top_builder_widget.builder_toolbar
        self.sequence_constructor = self.builder_toolbar.sequence_builder
        self.graph_editor = self.sequence_widget.sequence_modifier.graph_editor
        self.variation_manager = self.builder_toolbar.dictionary.variation_manager
        self.beat_frame = self.sequence_widget.beat_frame
        self.save_image_manager = self.beat_frame.export_manager
        self.indicator_label = self.sequence_widget.indicator_label
        self.print_sequence_manager = self.beat_frame.print_sequence_manager

    def _setup_buttons(self) -> None:
        self.buttons: list[SequenceWidgetButton] = []
        button_dict = {
            "add_to_dictionary": {
                "icon_path": "add_to_dictionary.svg",
                "callback": self.add_to_dictionary,
                "tooltip": "Add to Dictionary",
            },
            "save_image": {
                "icon_path": "save_image.svg",
                "callback": lambda: self.save_image_manager.save_image(),
                "tooltip": "Save Image",
            },
            # "print_sequence": {
            #     "icon_path": "print_sequence.svg",
            #     "callback": lambda: self.print_sequence_manager.print_sequence(),
            #     "tooltip": "Print Sequence",
            # },
            "clear_sequence": {
                "icon_path": "clear.svg",
                "callback": lambda: self.clear_sequence(show_indicator=True),
                "tooltip": "Clear Sequence",
            },
        }
        for button_name, button_data in button_dict.items():
            icon_path = f"images/icons/sequence_widget_icons/{button_data['icon_path']}"
            self._setup_button(
                button_name,
                icon_path,
                button_data["callback"],
                button_data["tooltip"],
            )

    def _setup_button(
        self, button_name: str, icon_path: str, callback, tooltip: str
    ) -> None:
        icon = QIcon(icon_path)
        button = SequenceWidgetButton(icon)
        button.clicked.connect(callback)
        button.setToolTip(tooltip)  # Set the tooltip for the button
        setattr(self, f"{button_name}_button", button)
        self.buttons.append(button)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        for button in self.buttons:
            self.layout.addWidget(button)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def add_to_dictionary(self) -> None:
        self.sequence = self.json_handler.load_current_sequence_json()

        base_pattern = "".join(
            pictograph.get("letter", "")
            for pictograph in self.sequence
            if "letter" in pictograph
        )
        if base_pattern:

            self.variation_manager.save_structural_variation(
                self.sequence, base_pattern
            )
            self.indicator_label.show_message(f"{base_pattern} added to dictionary!")

            self.main_widget.top_builder_widget.builder_toolbar.dictionary.reload_dictionary_tab()
        else:
            self.indicator_label.show_message(
                "You must build a sequence to add it to your dictionary."
            )

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        self._reset_beat_frame()
        if should_reset_to_start_pos_picker:
            self.sequence_constructor.reset_to_start_pos_picker()
        self.sequence_constructor.current_pictograph = self.beat_frame.start_pos
        self.json_handler.clear_current_sequence_file()
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")
        self._clear_graph_editor()

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_frame.beats:
            beat_view.setScene(None)
            beat_view.is_filled = False
        self.beat_frame.start_pos_view.setScene(None)
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_manager.deselect_beat()

    def _clear_graph_editor(self) -> None:
        self.graph_editor.GE_pictograph_view.set_to_blank_grid()
        self.graph_editor.adjustment_panel.update_turns_displays(0, 0)
        self.graph_editor.adjustment_panel.update_adjustment_panel()

    def resize_button_frame(self) -> None:
        button_height = self.height() // 9

        for button in self.buttons:
            button.setFixedSize(button_height, button_height)
            button.setIconSize((button.size() * 0.7))
            button.setStyleSheet(f"font-size: {self.font_size}px")

        self.layout.setSpacing(self.height() // 15)
