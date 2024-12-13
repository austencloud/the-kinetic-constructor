from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.sequence_generator.freeform.letter_type_button_widget import (
    LetterTypeButtonWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.sequence_generator.freeform.freeform_sequence_generator_frame import (
        FreeformSequenceGeneratorFrame,
    )
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class LetterTypePickerWidget(QWidget):
    def __init__(self, generator_frame: "FreeformSequenceGeneratorFrame"):
        super().__init__(generator_frame)
        self.generator_frame = generator_frame
        self.sequence_generator_settings = generator_frame.sequence_generator_settings
        self.builder_type = generator_frame.builder_type

        self.letter_mode_checkbox = QCheckBox("Filter Letter Types")
        self.letter_mode_checkbox.setChecked(True)
        self.letter_mode_checkbox.stateChanged.connect(self._on_letter_mode_changed)

        # Layout for letter type buttons
        self.letter_types_layout = QHBoxLayout()
        self.letter_types_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create 6 letter type button widgets
        self.letter_type_widgets: list[LetterTypeButtonWidget] = []
        for i, letter_type in enumerate(LetterType, start=1):
            w = LetterTypeButtonWidget(self, letter_type, i)
            w.clicked.connect(self._on_letter_type_clicked)
            self.letter_types_layout.addWidget(w)
            self.letter_type_widgets.append(w)

        # Initially hide these since default is "Use All Letters"
        self._set_letter_type_buttons_visible(False)

        # Main layout
        main_layout = QVBoxLayout(self)
        mode_layout = QHBoxLayout()
        mode_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_layout.addWidget(self.letter_mode_checkbox)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(self.letter_types_layout)
        main_layout.addStretch(1)

    def _on_letter_mode_changed(self, state):
        if not self.letter_mode_checkbox.isChecked():
            # All letters mode
            self._set_letter_type_buttons_visible(False)
            # self.sequence_generator_settings.set_sequence_generator_setting(
            #     "selected_letter_types", None, self.builder_type
            # )
        else:
            # Specific letters mode
            self._set_letter_type_buttons_visible(True)
            chosen = self.sequence_generator_settings.get_sequence_generator_setting(
                "selected_letter_types", self.builder_type
            )
            if chosen is None:
                # No previous selection, default all selected
                for w in self.letter_type_widgets:
                    w.is_selected = True
                    w.update_colors()
                self.sequence_generator_settings.set_sequence_generator_setting(
                    "selected_letter_types",
                    [lt.description for lt in LetterType],
                    self.builder_type,
                )
            else:
                # Restore previous selection
                any_selected = False
                for lt, w in zip(LetterType, self.letter_type_widgets):
                    is_selected = lt.description in chosen
                    w.is_selected = is_selected
                    w.update_colors()
                    if is_selected:
                        any_selected = True
                if not any_selected:
                    # None selected, select all
                    for w in self.letter_type_widgets:
                        w.is_selected = True
                        w.update_colors()
                    self.sequence_generator_settings.set_sequence_generator_setting(
                        "selected_letter_types",
                        [lt.description for lt in LetterType],
                        self.builder_type,
                    )

    def _on_letter_type_clicked(self, letter_type: LetterType, is_selected: bool):
        # Ensure at least one selected
        selected_count = sum(w.is_selected for w in self.letter_type_widgets)
        if selected_count == 0:
            # revert this one
            for lt, w in zip(LetterType, self.letter_type_widgets):
                if lt == letter_type:
                    w.is_selected = True
                    w.update_colors()

        chosen = [
            lt.description
            for lt, w in zip(LetterType, self.letter_type_widgets)
            if w.is_selected
        ]
        self.sequence_generator_settings.set_sequence_generator_setting(
            "selected_letter_types", chosen, self.builder_type
        )

    def _set_letter_type_buttons_visible(self, visible: bool):
        for w in self.letter_type_widgets:
            w.setVisible(visible)

    def apply_settings(self):
        selected_types = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "selected_letter_types", self.builder_type
            )
        )

        if selected_types is None:
            # all letters
            self.letter_mode_checkbox.setChecked(True)
            self._set_letter_type_buttons_visible(False)
        else:
            # specific letters
            self.letter_mode_checkbox.setChecked(False)
            self._set_letter_type_buttons_visible(True)
            if len(selected_types) > 0:
                any_selected = False
                for lt, w in zip(LetterType, self.letter_type_widgets):
                    is_selected = lt.description in selected_types
                    w.is_selected = is_selected
                    w.update_colors()
                    if is_selected:
                        any_selected = True
                if not any_selected:
                    # select all by default
                    for w in self.letter_type_widgets:
                        w.is_selected = True
                        w.update_colors()
                    self.sequence_generator_settings.set_sequence_generator_setting(
                        "selected_letter_types",
                        [lt.description for lt in LetterType],
                        self.builder_type,
                    )
            else:
                # none chosen, select all
                for w in self.letter_type_widgets:
                    w.is_selected = True
                    w.update_colors()
                self.sequence_generator_settings.set_sequence_generator_setting(
                    "selected_letter_types",
                    [lt.description for lt in LetterType],
                    self.builder_type,
                )

    def get_selected_letter_types(self) -> list[LetterType]:
        return [
            lt for lt, w in zip(LetterType, self.letter_type_widgets) if w.is_selected
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.generator_frame.height() // 25
        self.letter_mode_checkbox.setFont(QFont("Arial", font_size))
        self.layout().setSpacing(self.generator_frame.height() // 50)
        width = self.generator_frame.width() // 16
        for w in self.letter_type_widgets:
            w.setFixedSize(width, width)
            f = w.label.font()
            f.setPointSize(font_size)
            w.label.setFont(f)

        f = self.letter_mode_checkbox.font()
        f.setPointSize(font_size)
        self.letter_mode_checkbox.setFont(f)
