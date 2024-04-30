import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QEvent, QSize
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QApplication,
    QMessageBox,
)


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser import DictionaryBrowser


class ThumbnailBox(QWidget):
    def __init__(
        self, browser: "DictionaryBrowser", base_word, thumbnails, parent=None
    ):
        super().__init__(parent)
        self.base_word = base_word
        self.thumbnails = thumbnails
        self.current_index = 0
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.setup_ui()

    def setup_ui(self):
        self._setup_base_word_label()
        self._setup_slideshow_area()
        self._setup_navigation_buttons()
        self._setup_variation_number_label()
        self._setup_layout()
        self.setMouseTracking(True)
        self.thumbnail_label.installEventFilter(self)
        self.thumbnail_label.mousePressEvent = self.thumbnail_clicked

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.base_word_label)
        self.layout.addWidget(
            self.thumbnail_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addLayout(self.nav_layout)
        self.layout.addWidget(self.variation_number_label)
        # add stretch
        self.layout.addStretch()
        self.setLayout(self.layout)

    def _setup_variation_number_label(self):
        self.variation_number_label = QLabel(f"Variation {self.current_index + 1}")
        self.variation_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.variation_number_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))

    def _setup_navigation_buttons(self):
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.prev_thumbnail)
        self.prev_button.setStyleSheet("background-color: white;")
        self.prev_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))  # Add this line
        self.nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.next_thumbnail)
        self.next_button.setStyleSheet("background-color: white;")
        self.next_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))  # Add this line
        self.nav_layout.addWidget(self.next_button)

    def _setup_slideshow_area(self):
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setStyleSheet("border: 3px solid black;")
        self.update_thumbnail()

    def _setup_base_word_label(self):
        self.base_word_label = QLabel(self.base_word)
        self.base_word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.base_word_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

    def thumbnail_clicked(self, event):
        # Assuming the first thumbnail is the one to be displayed/edited
        metadata = self.use_pillow_to_extract_metadata_from_file(self.thumbnails[0])
        self.browser.dictionary_widget.thumbnail_clicked(
            QPixmap(self.thumbnails[self.current_index]), metadata
        )
        super().mousePressEvent(event)  # Ensure other mouse press events are handled

    def use_pillow_to_extract_metadata_from_file(self, file_path):
        from PIL import Image

        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
                else:
                    QMessageBox.warning(
                        self.browser.main_widget,
                        "Error",
                        "No sequence metadata found in the thumbnail.",
                    )
        except Exception as e:
            QMessageBox.critical(
                self.browser.main_widget,
                "Error",
                f"Error loading sequence from thumbnail: {e}",
            )

    def showEvent(self, event):
        super().showEvent(event)
        if self.isVisible():
            self.adjust_thumbnail_size()

    def adjust_thumbnail_size(self):
        if not hasattr(self, "initial_size_set") or not self.initial_size_set:
            initial_pixmap = (
                QPixmap(self.thumbnails[0]) if self.thumbnails else QPixmap()
            )
            initial_size = self.calculate_thumbnail_size(initial_pixmap.size())
            self.thumbnail_label.setFixedSize(initial_size)
            self.thumbnail_label.setPixmap(
                initial_pixmap.scaled(
                    initial_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.initial_size_set = True

    def calculate_thumbnail_size(self, pixmap_size):
        # Convert the pixmap size to integers
        pixmap_width = int(pixmap_size.width())
        pixmap_height = int(pixmap_size.height())

        # Calculate the size based on the scroll area's width instead of the dictionary widget
        scroll_area_width = (
            int(self.browser.scroll_area.viewport().width())
            - int(self.browser.scroll_layout.horizontalSpacing()) * 4
        )  # Account for spacing

        thumbnail_width = scroll_area_width // 3

        thumbnail_height = max(int(thumbnail_width * pixmap_height / pixmap_width), 150)

        return QSize(thumbnail_width, thumbnail_height)

    def eventFilter(self, obj, event):
        if obj == self.thumbnail_label and event.type() == QEvent.Type.Enter:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.thumbnail_label.setStyleSheet("border: 3px solid gold")
        elif obj == self.thumbnail_label and event.type() == QEvent.Type.Leave:
            self.unsetCursor()
            self.thumbnail_label.setStyleSheet("border: 3px solid black")
        return super().eventFilter(obj, event)

    def set_selected(self, selected):
        self.isSelected = selected
        self.update_ui()

    def update_thumbnail(self):
        if self.thumbnails:
            pixmap = QPixmap(self.thumbnails[self.current_index])
            self.thumbnail_label.setPixmap(
                pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def next_thumbnail(self):
        self.current_index = (self.current_index + 1) % len(self.thumbnails)
        self.update_thumbnail()

    def prev_thumbnail(self):
        self.current_index = (self.current_index - 1) % len(self.thumbnails)
        self.update_thumbnail()

    def update_thumbnail_size(self):
        # Update the thumbnail size according to the DictionaryWidget's layout.
        if self.thumbnails:
            initial_pixmap = QPixmap(self.thumbnails[0])
            thumbnail_width = self.browser.thumbnail_area_width()
            thumbnail_height = max(
                int(thumbnail_width * initial_pixmap.height() / initial_pixmap.width()),
                150,
            )
            new_size = QSize(thumbnail_width, thumbnail_height)
            self.thumbnail_label.setFixedSize(new_size)
            self.thumbnail_label.setPixmap(
                initial_pixmap.scaled(
                    new_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def showEvent(self, event):
        super().showEvent(event)
        # Delay the thumbnail size update until the DictionaryWidget has been laid out.
        QApplication.postEvent(self, QEvent(QEvent.Type.User))

    def event(self, event):
        if event.type() == QEvent.Type.User:
            self.update_thumbnail_size()
            return True
        return super().event(event)
