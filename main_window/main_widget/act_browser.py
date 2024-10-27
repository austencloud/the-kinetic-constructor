from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QSizePolicy
from main_window.main_widget.act_thumbnail_box import ActThumbnailBox
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_tab import ActTab


class ActBrowser(QScrollArea):
    def __init__(self, act_tab: "ActTab") -> None:
        super().__init__(act_tab)
        self.act_tab = act_tab
        self.thumbnail_boxes: list[ActThumbnailBox] = []
        self.metadata_extractor = MetaDataExtractor(self.act_tab.main_widget)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)

        # Set 0 margins and spacing to eliminate any implicit gaps
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self.scroll_content.setLayout(self.grid_layout)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._setup_layout()
        self.populate_favorites()
        # transparent back
        self.setStyleSheet("background-color: rgba(0,0,0,0);")

    def _setup_layout(self):
        self.setWidgetResizable(True)
        self.setWidget(self.scroll_content)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        print("ActBrowser layout setup complete.")

    def populate_favorites(self):
        # Clear any existing thumbnail boxes
        for box in self.thumbnail_boxes:
            box.setParent(None)

        self.thumbnail_boxes = []

        # Fetch sequences and add favorites only
        sequences = (
            self.act_tab.main_widget.dictionary_widget.browser.get_all_sequences()
        )
        print(f"Found {len(sequences)} sequences.")

        row, col = 0, 0
        max_columns = 2  # Number of thumbnails per row

        for sequence in sequences:
            thumbnails = sequence[1]
            is_favorite = self.metadata_extractor.get_favorite_status(thumbnails[0])

            if is_favorite:
                thumbnail_box = ActThumbnailBox(self, sequence[0], thumbnails)
                # Expanding size policy, but we'll fix the width later
                # thumbnail_box.setSizePolicy(
                #     QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
                # )

                self.thumbnail_boxes.append(thumbnail_box)
                self.grid_layout.addWidget(thumbnail_box, row, col)  # Remove AlignTop

                col += 1
                if col == max_columns:
                    col = 0
                    row += 1

    def resize_browser(self):
        """Dynamically resize each thumbnail to fit half of the ActBrowser's width."""
        scroll_bar_width = self.verticalScrollBar().width()
        browser_width = self.width() - scroll_bar_width
        for box in self.thumbnail_boxes:
            box.resize_thumbnail_box()
        self.scroll_content.setMinimumWidth(browser_width)
