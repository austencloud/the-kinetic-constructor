from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QPushButton,
    QFrame,
    QVBoxLayout,
    QApplication,
    QSpacerItem,
    QSizePolicy,
)
from .button_panel_placeholder import ButtonPanelPlaceholder
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .sequence_workbench import SequenceWorkbench


class SequenceWorkbenchButtonPanel(QFrame):
    swap_colors_button: QPushButton
    colors_swapped = False
    spacers: list[QSpacerItem] = []

    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sw = sequence_workbench
        self.main_widget = self.sw.main_widget
        self.beat_frame = self.sw.beat_frame
        self.export_manager = self.beat_frame.image_export_manager
        self.indicator_label = self.sw.indicator_label
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.font_size = self.sw.width() // 45
        self.top_placeholder = ButtonPanelPlaceholder(self)
        self.bottom_placeholder = ButtonPanelPlaceholder(self)
        self.buttons: dict[str, QPushButton] = {}
        self._setup_buttons()
        self._setup_layout()

    def _setup_buttons(self) -> None:
        button_data = {
            "add_to_dictionary": (
                "add_to_dictionary.svg",
                self.sw.add_to_dictionary_manager.add_to_dictionary,
                "Add to Dictionary",
            ),
            "save_image": (
                "save_image.svg",
                lambda: self.export_manager.dialog_executor.exec_dialog(
                    self.sw.main_widget.json_manager.loader_saver.load_current_sequence_json()
                ),
                "Save Image",
            ),
            "view_full_screen": (
                "eye.png",
                lambda: self.sw.full_screen_viewer.view_full_screen(),
                "View Full Screen",
            ),
            "mirror_sequence": (
                "mirror.png",
                lambda: self.sw.mirror_manager.reflect_current_sequence(),
                "Mirror Sequence",
            ),
            "swap_colors": (
                "yinyang1.svg",
                lambda: self.sw.color_swap_manager.swap_current_sequence(),
                "Swap Colors",
            ),
            "rotate_sequence": (
                "rotate.svg",
                lambda: self.sw.rotation_manager.rotate_current_sequence(),
                "Rotate Sequence",
            ),
            "delete_beat": (
                "delete.svg",
                lambda: self.sw.beat_deleter.delete_selected_beat(),
                "Delete Beat",
            ),
            "clear_sequence": (
                "clear.svg",
                lambda: self.clear_sequence(),
                "Clear Sequence",
            ),
        }

        for name, (icon, callback, tooltip) in button_data.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_workbench_icons/{icon}"
            )
            button = self._create_button(icon_path, callback, tooltip)
            setattr(self, f"{name}_button", button)
            self.buttons[name] = button

    def clear_sequence(self):
        sequence = (
            self.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(sequence) < 2:
            self.indicator_label.show_message("No sequence to clear")
            return

        if self.sw.graph_editor.is_toggled:
            self.sw.graph_editor.animator.toggle()

        self.indicator_label.show_message("Sequence cleared")
        self.sw.beat_deleter.start_position_deleter.delete_all_beats(
            show_indicator=True
        )

    def _create_button(self, icon_path: str, callback, tooltip: str) -> QPushButton:
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.enterEvent = lambda event: button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        button.leaveEvent = lambda event: button.setCursor(Qt.CursorShape.ArrowCursor)
        return button

    def toggle_swap_colors_icon(self):
        icon_name = "yinyang2.svg" if self.colors_swapped else "yinyang1.svg"
        new_icon_path = get_images_and_data_path(
            f"images/icons/sequence_workbench_icons/{icon_name}"
        )
        self.colors_swapped = not self.colors_swapped
        self.swap_colors_button.setIcon(QIcon(new_icon_path))
        QApplication.processEvents()

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.top_placeholder)

        button_groups = [
            ["add_to_dictionary", "save_image", "view_full_screen"],
            ["mirror_sequence", "swap_colors", "rotate_sequence"],
            ["delete_beat", "clear_sequence"],
        ]

        for group in button_groups:
            for name in group:
                layout.addWidget(self.buttons[name])
            spacer = QSpacerItem(
                20,
                self.sw.height() // 20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
            layout.addItem(spacer)

        layout.addWidget(self.bottom_placeholder)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        spacer = QSpacerItem(
            20,
            self.sw.height() // 40,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        layout.addItem(spacer)
        self.layout: QVBoxLayout = layout

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resize_button_panel()

    def resize_button_panel(self):
        button_size = self.sw.main_widget.height() // 20
        border_radius = button_size // 2
        button_style = f"""
            QPushButton {{
                border-radius: {border_radius}px;
                background-color: white;
                color: black;
                border: 1px solid #555;
            }}
            QPushButton:hover {{
                background-color: #F0F0F0;
            }}
            QPushButton:pressed {{
                background-color: #D0D0D0;
            }}
        """

        for button in self.buttons.values():
            button.setFixedSize(button_size, button_size)
            button.setIconSize(button.size() * 0.75)
            button.setStyleSheet(button_style)

        layout_spacing = self.sw.beat_frame.main_widget.height() // 120
        self.layout.setSpacing(layout_spacing)

        spacer_size = self.sw.beat_frame.main_widget.height() // 20
        for spacer in self.spacers:
            spacer.changeSize(
                20,
                spacer_size,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        self.layout.update()
