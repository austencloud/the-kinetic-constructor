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
        self.beat_frame = self.sequence_widget.beat_frame
        self._setup_components()
        self._setup_layout()

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
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.sequence_growth_checkbox.toggled.connect(self._toggle_grow_sequence)
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
        # set the number of beats dropdown to the current number of beats

    def _setup_layout_options_dropdown(self):
        self.layout_label = QLabel("Layout Options:")

        self.layout_combo_box = QComboBox(self)
        self.layout_combo_box.currentIndexChanged.connect(self.dialog.update_preview)

    def _toggle_grow_sequence(self):
        is_grow_sequence_checked = self.sequence_growth_checkbox.isChecked()

        self.beats_label.setEnabled(not is_grow_sequence_checked)
        self.beats_combo_box.setEnabled(not is_grow_sequence_checked)
        self.layout_label.setEnabled(not is_grow_sequence_checked)
        self.layout_combo_box.setEnabled(not is_grow_sequence_checked)

        color = "grey" if is_grow_sequence_checked else "black"
        self.beats_label.setStyleSheet(f"color: {color};")
        self.layout_label.setStyleSheet(f"color: {color};")

        if not is_grow_sequence_checked:
            num_beats = self.sequence_widget.beat_frame.find_next_available_beat() or 0
            self.beats_combo_box.setCurrentText(str(num_beats))
            self.dialog._setup_layout_options()
            layout_option = self.get_layout_option_from_current_beat_frame_layout()
            self.layout_combo_box.setCurrentText(layout_option)

        self.dialog.update_preview()

    def get_layout_option_from_current_beat_frame_layout(self):
        cols = self.beat_frame.layout_manager.get_cols()
        rows = self.beat_frame.layout_manager.get_rows()

        return f"{cols} x {rows}"

    def load_settings(self):
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self._toggle_grow_sequence()

    def initialize_from_state(self, state: dict):
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)

        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
        self._toggle_grow_sequence()

    def get_currently_visible_beats(self) -> int:
        # check the beat frame for beats that are visible
        num_beats = 0
        for beat in self.beat_frame.beats:
            if beat.isVisible():
                num_beats += 1
        return num_beats

    def showEvent(self, event):
        num_beats = self.get_currently_visible_beats()
        self.beats_combo_box.setCurrentText(str(num_beats))

        layout_option = self.get_layout_option_from_current_beat_frame_layout()
        self.layout_combo_box.setCurrentText(layout_option)
