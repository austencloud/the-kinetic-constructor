from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QFrame, QVBoxLayout
from circular_word_checker import CircularWordChecker
from widgets.path_helpers.path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SW_ActionButton(QPushButton):
    def __init__(self, icon_path: str):
        super().__init__()
        self.setIcon(QIcon(icon_path))

    def enterEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)


from PyQt6.QtWidgets import QMessageBox

from PyQt6.QtWidgets import QMessageBox


class SW_ButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget

        self.orientations = ["in", "counter", "out", "clock"]
        self.font_size = self.sequence_widget.width() // 45
        self.add_to_dictionary_manager = self.sequence_widget.add_to_dictionary_manager
        self._setup_dependencies()
        self._setup_buttons()
        self._setup_layout()

    def _setup_dependencies(self):
        self.main_widget = self.sequence_widget.main_widget
        self.json_manager = self.main_widget.json_manager
        self.sequence_builder = self.sequence_widget.top_builder_widget.sequence_builder
        self.beat_frame = self.sequence_widget.beat_frame
        self.export_manager = self.beat_frame.export_manager
        self.indicator_label = self.sequence_widget.indicator_label
        self.print_sequence_manager = self.beat_frame.print_sequence_manager
        self.settings_manager = self.main_widget.main_window.settings_manager

    def _setup_buttons(self) -> None:
        self.buttons: list[SW_ActionButton] = []
        button_dict = {
            "add_to_dictionary": {
                "icon_path": "add_to_dictionary.svg",
                "callback": self.add_to_dictionary_manager.add_to_dictionary,
                "tooltip": "Add to Dictionary",
            },
            "save_image": {
                "icon_path": "save_image.svg",
                "callback": lambda: self.export_manager.dialog_executor.exec_dialog(),
                "tooltip": "Save Image",
            },
            "layout_options": {
                "icon_path": "options.svg",
                "callback": self.sequence_widget.show_options_panel,
                "tooltip": "Layout Options",
            },
            "clear_sequence": {
                "icon_path": "clear.svg",
                "callback": lambda: self.clear_sequence(show_indicator=True),
                "tooltip": "Clear Sequence",
            },
            "magic_wand": {
                "icon_path": "magic_wand.svg",
                "callback": self.auto_complete_sequence,
                "tooltip": "Auto Complete Sequence",
            },
        }
        for button_name, button_data in button_dict.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_widget_icons/{button_data['icon_path']}"
            )
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
        button = SW_ActionButton(icon)
        button.clicked.connect(callback)
        button.setToolTip(tooltip)  # Set the tooltip for the button
        setattr(self, f"{button_name}_button", button)
        self.buttons.append(button)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        for button in self.buttons:
            self.layout.addWidget(button)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def auto_complete_sequence(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        checker = CircularWordChecker(sequence[1:])
        _, is_permutable = checker.check_properties()

        if is_permutable:
            self.sequence_widget.autocompleter.perform_auto_completion(sequence)
        else:
            QMessageBox.warning(
                self,
                "Auto-Complete Disabled",
                "The sequence is not permutable and cannot be auto-completed.",
            )

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        self._reset_beat_frame()

        if should_reset_to_start_pos_picker:
            self.sequence_builder.reset_to_start_pos_picker()
        self.sequence_builder.current_pictograph = self.beat_frame.start_pos
        self.json_manager.loader_saver.clear_current_sequence_file()
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")
        self._clear_graph_editor()

        # Reset the layout to the smallest possible amount
        if self.settings_manager.get_grow_sequence():
            self.beat_frame.layout_manager.configure_beat_frame(0)

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_frame.beats:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        self.beat_frame.start_pos_view.setScene(
            self.beat_frame.start_pos_view.blank_beat
        )
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_manager.deselect_beat()
        self.beat_frame.sequence_widget.update_current_word()

    def _clear_graph_editor(self) -> None:
        self.graph_editor = self.sequence_widget.graph_editor
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
