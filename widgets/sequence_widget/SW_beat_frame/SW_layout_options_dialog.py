from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCheckBox,
    QLabel,
    QGridLayout,
    QWidget,
    QComboBox,
)
from PyQt6.QtCore import Qt

from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from widgets.sequence_widget.SW_beat_frame.start_pos_beat import StartPositionBeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget

class SW_LayoutOptionsDialog(QDialog):
    def __init__(
        self, sequence_widget: "SequenceWidget", initial_state: Optional[dict] = None
    ):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = self.sequence_widget.main_widget.main_window.settings_manager
        self.setWindowTitle("Sequence Layout Options")
        self.layout_options = {
            1: [(1, 1)],
            2: [(1, 2)],
            3: [(1, 3), (2, 2)],
            4: [(2, 2), (1, 4)],
            6: [(3, 2), (2, 3)],
            8: [(4, 2), (2, 4)],
            7: [(4, 2), (2, 4)],
            9: [(3, 3), (2, 5), (5, 2)],
            10: [(5, 2), (2, 5)],
            11: [(4, 3), (3, 4)],
            12: [(4, 3), (3, 4)],
            13: [(5, 3), (3, 5)],
            14: [(4, 4), (2, 7), (7, 2)],
            15: [(5, 3), (3, 5)],
            16: [(4, 4), (2, 8), (8, 2)],
        }

        self._set_size()
        self._setup_preview_section()
        self._setup_options_section()
        self._setup_options_layout()
        self._setup_main_layout()
        self._setup_layout_options()

        if initial_state:
            self._initialize_from_state(initial_state)
        else:
            self._load_settings()

    def _load_settings(self):
        grow_sequence = self.settings_manager.get_grow_sequence()
        self.sequence_growth_checkbox.setChecked(grow_sequence)

    def apply_settings(self):
        grow_sequence = self.sequence_growth_checkbox.isChecked()
        self.settings_manager.set_grow_sequence(grow_sequence)
        num_beats = int(self.beats_combo_box.currentText())
        selected_layout = self.layout_combo_box.currentText()
        rows, cols = map(int, selected_layout.split(" x "))

        self.sequence_widget.apply_options(
            grow_sequence,
            rows,
            cols,
            num_beats,
            self.save_layout_checkbox.isChecked(),
        )
        self.accept()
    def _set_size(self):
        main_widget_size = self.sequence_widget.main_widget.size()
        self.setFixedSize(main_widget_size.width() // 2, main_widget_size.height() // 2)

    def _setup_main_layout(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.preview_section, 1)
        self.main_layout.addLayout(self.options_layout, 1)

    def _setup_preview_section(self):
        self.preview_section = QWidget()
        self.preview_layout = QGridLayout(self.preview_section)
        self.preview_layout.setSpacing(0)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_options_section(self):
        self.sequence_growth_checkbox = QCheckBox(
            "Grow sequence with added pictographs"
        )
        # TODO  set this to checked depending on  if it's already set in the settings

        self.sequence_growth_checkbox.toggled.connect(self.update_preview)
        self.beats_label = QLabel("Number of Beats:")
        self.beats_combo_box = QComboBox(self)
        self.beats_combo_box.addItems([str(i) for i in self.layout_options.keys()])
        self.beats_combo_box.currentIndexChanged.connect(self._setup_layout_options)
        self.layout_label = QLabel("Layout Options:")
        self.layout_combo_box = QComboBox(self)
        self.layout_combo_box.currentIndexChanged.connect(self.update_preview)
        self.save_layout_checkbox = QCheckBox("Save this layout as default")
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)

    def _setup_options_layout(self):
        self.options_layout = QVBoxLayout()
        self.options_layout.addStretch(1)
        self.options_layout.addWidget(self.sequence_growth_checkbox)
        self.options_layout.addWidget(self.beats_label)
        self.options_layout.addWidget(self.beats_combo_box)
        self.options_layout.addWidget(self.layout_label)
        self.options_layout.addWidget(self.layout_combo_box)
        self.options_layout.addWidget(self.save_layout_checkbox)
        self.options_layout.addWidget(self.apply_button)
        self.options_layout.addStretch(1)

    def _setup_layout_options(self):
        self.layout_combo_box.clear()
        num_beats = int(self.beats_combo_box.currentText())
        layouts = self.layout_options.get(num_beats, [])
        for layout in layouts:
            self.layout_combo_box.addItem(f"{layout[0]} x {layout[1]}")
        if layouts:
            self.layout_combo_box.setCurrentIndex(0)

    def update_preview(self):
        layout = self.preview_section.layout()
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        if not self.sequence_growth_checkbox.isChecked():
            num_beats = int(self.beats_combo_box.currentText())
            selected_layout = self.layout_combo_box.currentText()
            if selected_layout:
                rows, cols = map(int, selected_layout.split(" x "))

                cols_with_start_pos = cols + 1
                rows_with_start_pos = rows + 1
                preview_size = min(
                    (self.width() // 2) // cols_with_start_pos,
                    self.height() // rows_with_start_pos,
                )
                beat_size = preview_size

                if layout.count() == 0:
                    start_pos_view = StartPositionBeatView(
                        self.sequence_widget.beat_frame
                    )
                    start_pos_view.setFixedSize(beat_size, beat_size)
                    layout.addWidget(start_pos_view, 0, 0)

                    beat_number = 0
                    for row in range(rows):
                        for col in range(1, cols + 1):
                            if beat_number < num_beats:
                                beat_view = BeatView(self.sequence_widget.beat_frame)
                                beat_view.setFixedSize(beat_size, beat_size)
                                layout.addWidget(beat_view, row, col)
                                beat_number += 1

    def _initialize_from_state(self, state: dict):
        num_beats = state.get("num_beats", 0)
        rows = state.get("rows", 1)
        cols = state.get("cols", 1)
        grow_sequence = state.get("grow_sequence", False)
        save_layout = state.get("save_layout", False)

        self.sequence_growth_checkbox.setChecked(grow_sequence)
        self.beats_combo_box.setCurrentText(str(num_beats))
        self.layout_combo_box.setCurrentText(f"{rows} x {cols}")
        self.save_layout_checkbox.setChecked(save_layout)
        self.update_preview()

    def apply_settings(self):
        grow_sequence = self.sequence_growth_checkbox.isChecked()
        if grow_sequence:
            num_filled_beats = (
                self.sequence_widget.beat_frame.find_next_available_beat() - 1 or 0
            )
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
                num_filled_beats + 1
            )
            # set the beat_frame.grow_sequence to True
            self.sequence_widget.beat_frame.grow_sequence = True
        else:
            num_beats = int(self.beats_combo_box.currentText())
            selected_layout = self.layout_combo_box.currentText()
            rows, cols = map(int, selected_layout.split(" x "))

            self.sequence_widget.apply_options(
                grow_sequence,
                rows,
                cols,
                num_beats,
                self.save_layout_checkbox.isChecked(),
            )
        self.accept()
