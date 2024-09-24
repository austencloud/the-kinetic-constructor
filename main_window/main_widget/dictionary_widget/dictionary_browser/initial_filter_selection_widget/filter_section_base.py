from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QApplication,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class FilterSectionBase(QWidget):
    def __init__(
        self,
        initial_selection_widget: "DictionaryInitialSelectionsWidget",
        label_text: str,
    ):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self.browser = initial_selection_widget.browser
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.section_manager = self.browser.section_manager
        self.main_widget = initial_selection_widget.browser.main_widget
        self.metadata_extractor = self.main_widget.metadata_extractor
        self._setup_ui(label_text)

        self.initialized = False

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        # Create a top bar with the back button on the left
        top_bar_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(
            self.initial_selection_widget.show_filter_choice_widget
        )
        top_bar_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        # Add the label centered below the top bar
        self.header_label = QLabel(label_text)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        layout.addStretch(1)
        self.setLayout(layout)

        self.back_button.hide()
        self.header_label.hide()

    def add_buttons(self):
        # placeholder method, implemented in subclasses
        pass

    def resize_go_back_button(self):
        self.back_button.setFixedWidth(self.main_widget.width() // 20)
        self.back_button.setFixedHeight(self.main_widget.height() // 20)
        font = self.back_button.font()
        font.setPointSize(self.main_widget.width() // 120)
        self.back_button.setFont(font)
        # QApplication.processEvents()
