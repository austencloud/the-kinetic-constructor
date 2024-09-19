from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QFrame, QVBoxLayout

from utilities.path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class SequenceWidgetButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget

        self.font_size = self.sequence_widget.width() // 45
        self.add_to_dictionary_manager = self.sequence_widget.add_to_dictionary_manager
        self._setup_dependencies()
        self._setup_buttons()
        self._setup_layout()

    def _setup_dependencies(self):
        self.main_widget = self.sequence_widget.main_widget
        self.json_manager = self.main_widget.json_manager
        # self.sequence_builder = (
        #     self.sequence_widget.top_builder_widget.sequence_builder_tab_widget
        # )
        self.beat_frame = self.sequence_widget.beat_frame
        self.export_manager = self.beat_frame.image_export_manager
        self.indicator_label = self.sequence_widget.indicator_label
        self.settings_manager = self.main_widget.main_window.settings_manager

    def _setup_buttons(self) -> None:
        self.buttons: list[QPushButton] = []
        button_dict = {
            "add_to_dictionary": {
                "icon_path": "add_to_dictionary.svg",
                "callback": self.add_to_dictionary_manager.add_to_dictionary,
                "tooltip": "Add to Dictionary",
            },
            "save_image": {
                "icon_path": "save_image.svg",
                "callback": lambda: self.export_manager.dialog_executor.exec_dialog(
                    self.beat_frame.json_manager.loader_saver.load_current_sequence_json()
                ),
                "tooltip": "Save Image",
            },
            "layout_options": {
                "icon_path": "options.svg",
                "callback": self.sequence_widget.show_options_panel,
                "tooltip": "Layout Options",
            },
            # "auto_complete_sequence": {
            #     "icon_path": "magic_wand.svg",
            #     "callback": self.sequence_widget.autocompleter.auto_complete_sequence,
            #     "tooltip": "Auto Complete Sequence",
            # },
            # "auto_builder": {
            #     "icon_path": "auto_builder.png",
            #     "callback": self.open_auto_builder_selection,
            #     "tooltip": "Auto Builder",
            # },
            "clear_sequence": {
                "icon_path": "clear.svg",
                "callback": lambda: self.sequence_widget.sequence_clearer.clear_sequence(
                    show_indicator=True
                ),
                "tooltip": "Clear Sequence",
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
        button = QPushButton()
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        button.enterEvent = lambda event: button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        button.leaveEvent = lambda event: button.setCursor(Qt.CursorShape.ArrowCursor)
        button.setIcon(icon)
        setattr(self, f"{button_name}_button", button)
        self.buttons.append(button)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        for button in self.buttons:
            self.layout.addWidget(button)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resize_button_frame(self) -> None:
        button_size = self.sequence_widget.main_widget.height() // 16

        for button in self.buttons:
            button.setFixedSize(button_size, button_size)
            button.setIconSize((button.size() * 0.7))
            button.setStyleSheet(f"font-size: {self.font_size}px")

        self.layout.setSpacing(self.sequence_widget.height() // 24)
