from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QFrame, QVBoxLayout, QApplication

from main_window.main_widget.sequence_widget.beat_frame.layout_options_dialog import (
    LayoutOptionsDialog,
)
from main_window.main_widget.sequence_widget.full_screen_viewer import FullScreenViewer
from main_window.main_widget.sequence_widget.sequence_color_swapper import (
    SequenceColorSwapper,
)
from main_window.main_widget.sequence_widget.sequence_rotater import SequenceRotator

from .sequence_mirror import SequenceMirror
from .button_panel_placeholder import ButtonPanelPlaceholder
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetButtonPanel(QFrame):
    swap_colors_button: QPushButton

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.placeholder = ButtonPanelPlaceholder(self)

        self.font_size = self.sequence_widget.width() // 45
        self._setup_dependencies()
        self.colors_swapped = False  # Add this flag
        self._setup_buttons()
        self.top_placeholder = ButtonPanelPlaceholder(self)
        self.bottom_placeholder = ButtonPanelPlaceholder(self)
        self._setup_layout()

    def _setup_dependencies(self):
        self.main_widget = self.sequence_widget.main_widget
        self.json_manager = self.main_widget.json_manager
        self.beat_frame = self.sequence_widget.beat_frame
        self.export_manager = self.beat_frame.image_export_manager
        self.indicator_label = self.sequence_widget.indicator_label
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.sequence_mirror = SequenceMirror()
        self.full_screen_viewer = FullScreenViewer(self.sequence_widget)
        self.color_swapper = SequenceColorSwapper()
        self.sequence_rotator = SequenceRotator()

    def _setup_buttons(self) -> None:
        self.buttons: list[QPushButton] = []
        button_dict = {
            "add_to_dictionary": {
                "icon": "add_to_dictionary.svg",
                "callback": self.sequence_widget.add_to_dictionary_manager.add_to_dictionary,
                "tooltip": "Add to Dictionary",
            },
            "save_image": {
                "icon": "save_image.svg",
                "callback": lambda: self.export_manager.dialog_executor.exec_dialog(
                    self.beat_frame.json_manager.loader_saver.load_current_sequence_json()
                ),
                "tooltip": "Save Image",
            },
            "layout_options": {
                "icon": "options.svg",
                "callback": self.show_options_panel,
                "tooltip": "Layout Options",
            },
            "view_full_screen": {
                "icon": "eye.png",
                "callback": self.full_screen_viewer.view_full_screen,
                "tooltip": "View Full Screen",
            },
            "mirror_sequence": {
                "icon": "mirror.png",
                "callback": self.mirror_current_sequence,
                "tooltip": "Mirror Sequence",
            },
            "swap_colors": {
                "icon": "yinyang1.png",  # Updated icon filename
                "callback": self.swap_colors_in_sequence,
                "tooltip": "Swap Colors",
            },
            "rotate_sequence": {
                "icon": "rotate.png",  # You'll need to provide an icon for rotation
                "callback": self.rotate_current_sequence,
                "tooltip": "Rotate Sequence",
            },
            "delete_beat": {
                "icon": "delete.svg",
                "callback": lambda: self.beat_frame.beat_deletion_manager.delete_selected_beat(),
                "tooltip": "Delete Beat",
            },
            "clear_sequence": {
                "icon": "clear.svg",
                "callback": lambda: self.sequence_widget.sequence_clearer.clear_sequence(
                    show_indicator=True
                ),
                "tooltip": "Clear Sequence",
            },
        }
        for button_name, button_data in button_dict.items():
            icon = get_images_and_data_path(
                f"images/icons/sequence_widget_icons/{button_data['icon']}"
            )
            self._setup_button(
                button_name,
                icon,
                button_data["callback"],
                button_data["tooltip"],
            )

    def show_options_panel(self) -> None:
        self.options_panel = LayoutOptionsDialog(self.sequence_widget)
        self.options_panel.exec()

    def mirror_current_sequence(self):
        current_sequence_json = (
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence_json) < 2:
            self.indicator_label.show_message("No sequence to mirror.")
            return

        mirrored_sequence_json = self.sequence_mirror.mirror_sequence(
            current_sequence_json
        )
        self.update_beats_in_place(mirrored_sequence_json)
        self.indicator_label.show_message("Sequence mirrored successfully!")

    def swap_colors_in_sequence(self):
        current_sequence_json = (
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence_json) < 2:
            self.indicator_label.show_message("No sequence to swap colors.")
            return

        swapped_sequence_json = self.color_swapper.swap_colors(current_sequence_json)
        self.update_beats_in_place(swapped_sequence_json)
        self.indicator_label.show_message("Colors swapped successfully!")
        self.toggle_swap_colors_icon()
        currently_selected_beat = (
            self.sequence_widget.beat_frame.selection_overlay.get_selected_beat()
        )
        self.sequence_widget.graph_editor.adjustment_panel.update_turns_panel(
            currently_selected_beat.beat.blue_motion,
            currently_selected_beat.beat.red_motion,
        )

    def rotate_current_sequence(self):
        current_sequence_json = (
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence_json) < 2:
            self.indicator_label.show_message("No sequence to rotate.")
            return

        rotated_sequence_json = self.sequence_rotator.rotate_sequence(
            current_sequence_json
        )
        self.update_beats_in_place(rotated_sequence_json)
        self.indicator_label.show_message("Sequence rotated successfully!")

    def update_beats_in_place(self, modified_sequence_json):
        beat_frame = self.sequence_widget.beat_frame
        beats = beat_frame.beats

        if len(modified_sequence_json) > 1:
            start_pos_dict = modified_sequence_json[1]
            beat_frame.start_pos_view.start_pos.updater.update_pictograph(
                start_pos_dict
            )

        for i, beat_dict in enumerate(modified_sequence_json[2:], start=0):
            if i < len(beats) and beats[i].is_filled:
                beats[i].beat.updater.update_pictograph(beat_dict)
            else:
                break 

        self.json_manager.loader_saver.save_current_sequence(modified_sequence_json)
        self.json_manager.ori_validation_engine.run(is_current_sequence=True)

        self.sequence_widget.current_word_label.update_current_word_label_from_beats()
        self.sequence_widget.difficulty_label.update_difficulty_label()

        self.sequence_widget.main_widget.manual_builder.option_picker.update_option_picker()

    def toggle_swap_colors_icon(self):
        if self.colors_swapped:
            new_icon_path = get_images_and_data_path(
                "images/icons/sequence_widget_icons/yinyang1.png"
            )
            self.colors_swapped = False
        else:
            new_icon_path = get_images_and_data_path(
                "images/icons/sequence_widget_icons/yinyang2.png"
            )
            self.colors_swapped = True
        new_icon = QIcon(new_icon_path)
        self.swap_colors_button.setIcon(new_icon)
        QApplication.processEvents()

    def _setup_button(
        self, button_name: str, icon_path: str, callback, tooltip: str
    ) -> None:
        icon = QIcon(icon_path)
        button = QPushButton()
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        button.enterEvent = lambda event: button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        button.leaveEvent = lambda event: button.setCursor(Qt.CursorShape.ArrowCursor)
        button.setIcon(icon)
        setattr(self, f"{button_name}_button", button)  # Assign to self
        self.buttons.append(button)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.top_placeholder)
        for button in self.buttons:
            self.layout.addWidget(button)
        self.layout.addWidget(self.bottom_placeholder)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(self.sequence_widget.height() // 40)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resize_button_panel()

    def resize_button_panel(self):
        button_size = self.sequence_widget.main_widget.height() // 24
        for button in self.buttons:
            button.setFixedSize(button_size, button_size)
            button.setIconSize(button.size() * 0.7)
            button.setStyleSheet(f"font-size: {self.font_size}px")

        spacing = self.sequence_widget.beat_frame.main_widget.height() // 100
        self.layout.setSpacing(spacing)

        self.layout.update()
