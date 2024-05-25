from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QPushButton,
    QWidget, QHBoxLayout
)

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_layout_options_dialog import (
        SW_LayoutOptionsDialog,
    )


class LayoutOptionsPanel(QWidget):
    def __init__(self, dialog: "SW_LayoutOptionsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sequence_widget = dialog.sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.layout_options = dialog.layout_options

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self._setup_grow_sequence_checkbox()
        self._setup_number_of_beats_dropdown()
        self._setup_layout_options_dropdown()
        self._setup_cancel_button()
        self._setup_apply_button()


    def _setup_layout(self):
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.combobox_layout = self._setup_combobox_layout()
        self.action_button_layout = self._setup_action_button_layout()

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.sequence_growth_checkbox)
        self.main_layout.addLayout(self.combobox_layout)
        self.main_layout.addLayout(self.action_button_layout)
        self.main_layout.addStretch(1)

    def _setup_action_button_layout(self):
        action_button_layout = QHBoxLayout()
        action_button_layout.addWidget(self.cancel_button)
        action_button_layout.addWidget(self.apply_button)
        return action_button_layout

    def _setup_combobox_layout(self):
        beats_vbox = QVBoxLayout()
        layout_options_vbox = QVBoxLayout()
        combobox_hbox = QHBoxLayout()

        beats_vbox.addWidget(self.beats_label)
        beats_vbox.addWidget(self.beats_combo_box)

        layout_options_vbox.addWidget(self.layout_label)
        layout_options_vbox.addWidget(self.layout_combo_box)

        combobox_hbox.addLayout(beats_vbox)
        combobox_hbox.addLayout(layout_options_vbox)
        return combobox_hbox


    def _setup_grow_sequence_checkbox(self):
        self.sequence_growth_checkbox = QCheckBox(
            "Grow sequence with added pictographs"
        )
        grow_sequence = self.settings_manager.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.sequence_growth_checkbox.toggled.connect(self.dialog.update_preview)

    def _setup_number_of_beats_dropdown(self):
        self.beats_label = QLabel("Number of Beats:")

        self.beats_combo_box = QComboBox(self)
        self.beats_combo_box.addItems([str(i) for i in self.layout_options.keys()])
        self.beats_combo_box.currentIndexChanged.connect(
            self.dialog._setup_layout_options
        )

    def _setup_layout_options_dropdown(self):
        self.layout_label = QLabel("Layout Options:")

        self.layout_combo_box = QComboBox(self)
        self.layout_combo_box.currentIndexChanged.connect(self.dialog.update_preview)

    def _setup_cancel_button(self):
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.dialog.close)

    def _setup_apply_button(self):
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.dialog.apply_settings)

    def load_settings(self):
        grow_sequence = self.settings_manager.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)

    def initialize_from_state(self, state: dict):
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)
        save_layout = state.get("save_layout", False)

        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
