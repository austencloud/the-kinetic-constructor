from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryWordLengthSelectorWidget(QWidget):
    def __init__(self, dictionary: "Dictionary") -> None:
        super().__init__(dictionary)
        self.dictionary = dictionary
        self.main_widget = dictionary.main_widget
        self.sort_manager = dictionary.sort_manager
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout = QHBoxLayout()
        word_lengths = [2, 3, 4, 5, 6, 7, 8]
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        for length in word_lengths:
            button = QPushButton(f"{length} letters")
            button.setCheckable(True)
            button.setChecked(visibility_settings.get(length, False))
            button.toggled.connect(
                lambda checked, length=length: self.toggle_word_length_visibility(
                    length, checked
                )
            )
            self.layout.addWidget(button)

        self.setLayout(self.layout)

    def toggle_word_length_visibility(self, length, visible) -> None:
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        visibility_settings[str(length)] = visible
        self.main_widget.main_window.settings_manager.set_word_length_visibility(
            visibility_settings
        )
        self.sort_manager.filter_sequences_by_length()
