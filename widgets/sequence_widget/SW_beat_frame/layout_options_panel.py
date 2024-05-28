from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

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
        # self._update_comboboxes_state()

    def _setup_components(self):
        self._setup_grow_sequence_checkbox()
        self._setup_number_of_beats_dropdown()
        self._setup_layout_options_dropdown()

    def _setup_layout(self):
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.combobox_layout = self._setup_combobox_layout()

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.checkbox_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addLayout(self.combobox_layout)
        self.main_layout.addStretch(1)

    def _setup_combobox_layout(self):
        beats_vbox = QVBoxLayout()
        layout_options_vbox = QVBoxLayout()
        combobox_hbox = QHBoxLayout()

        beats_vbox.addWidget(self.beats_label)
        beats_vbox.addWidget(self.beats_combo_box)
        beats_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_options_vbox.addWidget(self.layout_label)
        layout_options_vbox.addWidget(self.layout_combo_box)
        layout_options_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combobox_hbox.addStretch(3)
        combobox_hbox.addLayout(beats_vbox)
        combobox_hbox.addStretch(1)
        combobox_hbox.addLayout(layout_options_vbox)
        combobox_hbox.addStretch(3)
        return combobox_hbox

    def _setup_grow_sequence_checkbox(self):
        self.sequence_growth_checkbox = QCheckBox("Grow sequence")
        grow_sequence = self.settings_manager.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.sequence_growth_checkbox.toggled.connect(self._update_comboboxes_state)
        font = self.sequence_growth_checkbox.font()
        font_size = self.sequence_widget.width() // 60
        font.setPointSize(font_size)
        self.sequence_growth_checkbox.setFont(font)
        # increase the checkbox size
        self.sequence_growth_checkbox.setStyleSheet(
            f"QCheckBox::indicator {{ width: {font_size}px; height: {font_size}px; }}"
        )

        self.checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(self.checkbox_widget)
        checkbox_layout.addWidget(self.sequence_growth_checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def _update_comboboxes_state(self):
        is_grow_sequence_checked = self.sequence_growth_checkbox.isChecked()
        state = not is_grow_sequence_checked

        self.beats_label.setEnabled(state)
        self.beats_combo_box.setEnabled(state)
        self.layout_label.setEnabled(state)
        self.layout_combo_box.setEnabled(state)

        color = "grey" if not state else "black"
        self.beats_label.setStyleSheet(f"color: {color};")
        self.layout_label.setStyleSheet(f"color: {color};")
        self.dialog.update_preview()

    def load_settings(self):
        grow_sequence = self.settings_manager.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self._update_comboboxes_state()

    def initialize_from_state(self, state: dict):
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)
        save_layout = state.get("save_layout", False)

        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
        self._update_comboboxes_state()
