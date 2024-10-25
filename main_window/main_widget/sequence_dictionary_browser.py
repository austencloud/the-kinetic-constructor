from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea

from main_window.main_widget.write_tab_thumbnail_box import WriteTabThumbnailBox

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class SequenceDictionaryBrowser(QScrollArea):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.thumbnail_boxes: list[WriteTabThumbnailBox] = []

        self._setup_components()
        self._setup_layout()
        self.populate_dictionary()

    def _setup_components(self):
        self.grid_layout = QGridLayout()  # Use a grid layout for thumbnails

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addLayout(self.grid_layout)
        self.setLayout(layout)

    def populate_dictionary(self):
        # Clear the current thumbnail boxes
        for box in self.thumbnail_boxes:
            box.setParent(None)

        self.thumbnail_boxes = []

        sequences = (
            self.write_tab.main_widget.dictionary_widget.browser.get_all_sequences()
        )

        # Populate grid with SequenceThumbnailBox widgets
        row = 0
        col = 0
        max_columns = 3  # Set how many thumbnails per row

        for sequence in sequences:
            thumbnails = sequence[1]  # Assuming sequence[1] is a list of thumbnails
            thumbnail_box = WriteTabThumbnailBox(self, sequence[0], thumbnails)
            self.thumbnail_boxes.append(thumbnail_box)

            self.grid_layout.addWidget(thumbnail_box, row, col)

            col += 1
            if col == max_columns:
                col = 0
                row += 1

    def resize_browser(self):
        # Adjust the thumbnail box sizes on window resize if necessary
        for box in self.thumbnail_boxes:
            box.resize_thumbnail_box()
