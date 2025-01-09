from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from data.beat_frame_layouts import beat_frame_layout_options
from main_window.main_widget.settings_dialog.beat_layout_tab.grow_sequence_checkbox import (
    GrowSequenceCheckbox,
)


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.beat_layout_tab import (
        BeatLayoutTab,
    )


class BeatLayoutControlPanel(QWidget):
    """Displays the 'grow sequence' checkbox, the number of beats dropdown,
    and the layout options dropdown in the layout options dialog."""

    def __init__(self, tab: "BeatLayoutTab"):
        super().__init__(tab)
        self.tab = tab
        self.sequence_widget = tab.sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.beat_frame = self.sequence_widget.beat_frame

        self._initialize_components()
        self._setup_layout()
        self._setup_layout_options()
        self._attach_listeners()

    def _attach_listeners(self):
        self.grow_sequence_checkbox.toggled.connect(
            self.grow_sequence_checkbox.toggle_grow_sequence
        )
        self.beats_combo_box.currentIndexChanged.connect(self._setup_layout_options)

    def _initialize_components(self):
        """Initialize all UI components."""
        self.beats_label = QLabel("Number of Beats:")
        self.layout_label = QLabel("Beat Layout Options:")
        self.beats_combo_box = QComboBox(self)
        self.layout_combo_box = QComboBox(self)

        self._setup_grow_sequence_checkbox()
        self._setup_number_of_beats_dropdown()
        self._setup_layout_options_dropdown()

    def _setup_layout(self):
        """Setup the layout of the UI components."""
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.combobox_layout = self._setup_combobox_layout()

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.checkbox_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addLayout(self.combobox_layout)
        self.main_layout.addStretch(1)

    def _setup_layout_options(self):
        """Setup the layout options in the combo box."""
        self.layout_combo_box.clear()
        num_beats = int(self.beats_combo_box.currentText())
        layouts = beat_frame_layout_options.get(num_beats, [])
        for layout in layouts:
            self.layout_combo_box.currentIndexChanged.disconnect(
                self.tab.beat_frame.update_preview
            )
            self.layout_combo_box.addItem(f"{layout[0]} x {layout[1]}")
            self.layout_combo_box.currentIndexChanged.connect(
                self.tab.beat_frame.update_preview
            )
        if layouts:
            self.layout_combo_box.setCurrentIndex(0)
            self.save_layout_setting()

    def _setup_combobox_layout(self):
        """Setup the layout for the combo boxes."""
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
        self.grow_sequence_checkbox = GrowSequenceCheckbox(self)

        self.checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(self.checkbox_widget)
        checkbox_layout.addWidget(self.grow_sequence_checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_number_of_beats_dropdown(self):
        self.beats_combo_box.addItems(
            [str(i) for i in beat_frame_layout_options.keys()]
        )

        self.beats_combo_box.blockSignals(True)
        saved_beats = self.settings_manager.sequence_layout.get_layout_setting(
            "num_beats"
        )
        self.beats_combo_box.setCurrentText(str(saved_beats))
        self.beats_combo_box.blockSignals(False)

    def _setup_layout_options_dropdown(self):
        self.layout_combo_box.currentIndexChanged.connect(
            self.tab.beat_frame.update_preview
        )

        saved_layout = self.settings_manager.sequence_layout.get_layout_setting(
            "layout_option"
        )
        self.layout_combo_box.setCurrentText(saved_layout)

    def get_layout_option_from_current_sequence_beat_frame_layout(self):
        cols = self.beat_frame.layout_manager.get_cols()
        rows = self.beat_frame.layout_manager.get_rows()
        return f"{cols} x {rows}"

    def load_settings(self):
        grow_sequence = self.settings_manager.sequence_layout.get_layout_setting(
            "grow_sequence"
        )
        self.grow_sequence_checkbox.setChecked(grow_sequence)
        self.grow_sequence_checkbox.toggle_grow_sequence()

    def initialize_from_state(self, state: dict):
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)

        self.grow_sequence_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
        self.grow_sequence_checkbox.toggle_grow_sequence()

    def get_currently_visible_beats(self) -> int:
        num_beats = 0
        for beat in self.beat_frame.beat_views:
            if beat.isVisible():
                num_beats += 1
        return num_beats

    def save_layout_setting(self):
        num_beats = int(self.beats_combo_box.currentText())
        layout_option = self.layout_combo_box.currentText()
        self.settings_manager.sequence_layout.set_layout_setting("num_beats", num_beats)
        self.settings_manager.sequence_layout.set_layout_setting(
            "layout_option", layout_option
        )
