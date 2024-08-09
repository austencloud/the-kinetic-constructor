from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
import os
from typing import TYPE_CHECKING, List
from widgets.main_widget.sequence_card_tab.sequence_card_image_populator import (
    SequenceCardImagePopulator,
)
from widgets.main_widget.sequence_card_tab.sequence_card_tab_page_factory import (
    SequenceCardTabPageFactory,
)
from widgets.main_widget.sequence_card_tab.sequence_card_image_exporter import (
    SequenceCardTabImageExporter,
)
from widgets.main_widget.sequence_card_tab.sequence_card_tab_nav_sidebar import (
    SequenceCardTabNavSidebar,
)
from widgets.path_helpers.path_helpers import get_sequence_card_image_exporter_path

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceCardTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.nav_sidebar = SequenceCardTabNavSidebar(self)
        self.page_factory = SequenceCardTabPageFactory(self)
        self.image_exporter = SequenceCardTabImageExporter(self)
        self.populator = SequenceCardImagePopulator(self)
        self.pages: List[QWidget] = []
        self.init_ui()
        self.pages_cache: dict[int, List[QWidget]] = (
            {}
        )  # Cache QWidgets instead of layouts
        self.initialized = False

    def init_ui(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.nav_sidebar, 1)
        self.layout.addWidget(self.scroll_area, 15)

    def load_images(self):
        self.setCursor(Qt.CursorShape.WaitCursor)

        selected_length = self.nav_sidebar.selected_length

        # Check if pages for the selected length are already cached
        if selected_length in self.pages_cache:
            self.display_cached_pages(selected_length)
        else:
            export_path = get_sequence_card_image_exporter_path()
            images = self.get_all_images(export_path)
            self.display_images(images)
            # Cache the pages for future use
            self.pages_cache[selected_length] = self.pages.copy()

        self.setCursor(Qt.CursorShape.ArrowCursor)

    def display_cached_pages(self, selected_length: int):
        """Display the cached pages without recalculating."""
        for i in range(0, len(self.pages_cache[selected_length]), 2):
            # Create a new row layout for each pair of pages
            row_layout = QHBoxLayout()
            row_layout.setSpacing(self.margin)
            row_layout.setContentsMargins(
                self.margin, self.margin, self.margin, self.margin
            )

            for j in range(2):  # Only add up to two items per row
                if i + j < len(self.pages_cache[selected_length]):
                    page_widget = self.pages_cache[selected_length][i + j]
                    row_layout.addWidget(page_widget)

            self.scroll_layout.addLayout(row_layout)

    def get_all_images(self, path: str) -> List[str]:
        images = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root, file))
        return images

    def display_images(self, images: List[str]):
        filtered_images = [
            img_path
            for img_path in images
            if self.get_sequence_length(img_path) == self.nav_sidebar.selected_length
        ]
        sorted_images = sorted(
            filtered_images, key=lambda img_path: self.get_sequence_length(img_path)
        )

        total_width = self.main_widget.width()
        self.margin = total_width // 50
        self.page_width = (
            (total_width // 2) - (2 * self.margin) - (self.nav_sidebar.width() // 2)
        )
        self.page_height = int(self.page_width * 11 / 8.5)
        self.image_card_margin = self.page_width // 40

        self.populator.current_page_index = -1
        self.pages.clear()

        for image_path in sorted_images:
            pixmap = QPixmap(image_path)

            max_image_width = self.page_width // 2 - self.image_card_margin
            scale_factor = max_image_width / pixmap.width()
            scaled_height = int(pixmap.height() * scale_factor)

            if scaled_height + self.margin * 2 > self.page_height // 3:
                num_rows = self.get_num_rows_based_on_sequence_length(
                    self.nav_sidebar.selected_length
                )
                scaled_height = int(self.page_height // num_rows - self.margin * 2)
                scale_factor = scaled_height / pixmap.height()
                max_image_width = int(
                    pixmap.width() * scale_factor - self.image_card_margin
                )

            scaled_pixmap = pixmap.scaled(
                max_image_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            label = QLabel(self)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add the image to the layout
            self.populator.add_image_to_page(
                label,
                self.nav_sidebar.selected_length,
                scaled_pixmap,
                max_images_per_row=2,
            )

        # Cache the pages after they are created
        self.pages_cache[self.nav_sidebar.selected_length] = self.pages.copy()

    def get_num_rows_based_on_sequence_length(self, sequence_length: int) -> int:
        num_rows_per_length = {
            4: 7,
            8: 5,
            16: 2,
        }
        return num_rows_per_length.get(sequence_length, 4)

    def get_sequence_length(self, image_path: str) -> int:
        return self.main_widget.metadata_extractor.get_sequence_length(image_path)

    def refresh_sequence_cards(self):
        """Refresh the displayed sequence cards based on selected options."""
        selected_length = self.nav_sidebar.selected_length

        for page_widget in self.pages:
            if page_widget is not None:
                page_widget.setParent(None)

        # If the pages are cached, no need to clear and recalculate
        if selected_length in self.pages_cache:
            self.pages = self.pages_cache[selected_length]
            self.display_cached_pages(selected_length)
            return

        # Clear existing layouts and recalculate if not cached
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)
            widget = layout_item.widget()
            if widget is not None:
                widget.setParent(None)  # Properly remove the widget
            else:
                self.scroll_layout.removeItem(layout_item)
                sub_layout = layout_item.layout()
                if sub_layout is not None:
                    while sub_layout.count():
                        sub_item = sub_layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.setParent(None)

        self.pages.clear()
        self.load_images()

    def showEvent(self, event):
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.refresh_sequence_cards()
            self.initialized = True
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().showEvent(event)

    def paintEvent(self, event) -> None:
        self.background_manager = self.global_settings.setup_background_manager(self)
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)