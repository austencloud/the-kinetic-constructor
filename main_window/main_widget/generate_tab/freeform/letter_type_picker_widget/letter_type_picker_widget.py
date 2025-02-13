from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Adjust import to your actual project structure
from Enums.letters import LetterType
from .letter_type_button_widget import LetterTypeButtonWidget

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class LetterTypePickerWidget(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(generate_tab)
        self.generate_tab = generate_tab
        self.settings = generate_tab.settings

        self.filter_label = QLabel("Filter by type:")
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.letter_types_layout = QHBoxLayout()
        self.letter_types_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.letter_type_widgets: list[LetterTypeButtonWidget] = []
        for i, letter_type in enumerate(LetterType, start=1):
            w = LetterTypeButtonWidget(self, letter_type, i)
            w.clicked.connect(self._on_letter_type_clicked)
            self.letter_types_layout.addWidget(w)
            self.letter_type_widgets.append(w)

        main_layout = QVBoxLayout(self)
        mode_layout = QHBoxLayout()
        mode_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_layout.addWidget(self.filter_label)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(self.letter_types_layout)

    def _on_letter_type_clicked(self, letter_type: LetterType):
        selected_count = sum(w.is_selected for w in self.letter_type_widgets)
        if selected_count == 0:
            # Prevent deselecting all
            for lt, w in zip(LetterType, self.letter_type_widgets):
                if lt == letter_type:
                    w.is_selected = True
                    w.updater.update_colors()

        chosen = [
            lt.description
            for lt, w in zip(LetterType, self.letter_type_widgets)
            if w.is_selected
        ]
        self.settings.set_setting(
            "selected_letter_types",
            chosen,
        )

    def _set_letter_type_buttons_visible(self, visible: bool):
        for w in self.letter_type_widgets:
            w.setVisible(visible)

    def set_selected_types(self, selected_types: list[str]) -> None:
        """Sets which letter types are initially selected."""
        self._set_letter_type_buttons_visible(selected_types is not None)
        if selected_types:
            any_selected = False
            for lt, w in zip(LetterType, self.letter_type_widgets):
                is_selected = lt.description in selected_types
                w.is_selected = is_selected
                w.updater.update_colors()
                if is_selected:
                    any_selected = True
            if not any_selected:
                self._select_all_letter_types()
        else:
            self._select_all_letter_types()

    def _select_all_letter_types(self):
        """Selects all letter types if no saved preference is found."""
        descriptions = [lt.description for lt in LetterType]
        for w in self.letter_type_widgets:
            w.is_selected = True
            w.updater.update_colors()
        self.settings.set_setting("selected_letter_types", descriptions)

    def get_selected_letter_types(self) -> list[LetterType]:
        """Return a list of letter types that are currently selected."""
        return [
            lt for lt, w in zip(LetterType, self.letter_type_widgets) if w.is_selected
        ]

    def resizeEvent(self, event):
        """Resize child widgets, fonts, spacing, etc."""
        super().resizeEvent(event)
        font_size = self.generate_tab.main_widget.height() // 50
        self.filter_label.setFont(QFont("Arial", font_size))
        self.layout().setSpacing(font_size)

        # Dynamically size each button
        width = self.generate_tab.width() // 16
        for w in self.letter_type_widgets:
            w.setFixedSize(width, width)
            f = w.label.font()
            f.setBold(True)
            f.setPointSize(font_size)
            w.label.setFont(f)

        # Update filter label color
        global_settings = (
            self.generate_tab.main_widget.main_window.settings_manager.global_settings
        )
        color = self.generate_tab.main_widget.font_color_updater.get_font_color(
            global_settings.get_background_type()
        )
        existing_style = self.filter_label.styleSheet()
        new_style = f"{existing_style} color: {color};"
        self.filter_label.setStyleSheet(new_style)
