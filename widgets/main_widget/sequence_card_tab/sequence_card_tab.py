from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List
from .sequence_card_image_displayer import SequenceCardImageDisplayer
from .sequence_card_image_populator import SequenceCardImagePopulator
from .sequence_card_cached_page_displayer import SequenceCardCachedPageDisplayer
from .sequence_card_refresher import SequenceCardRefresher
from .sequence_card_page_factory import SequenceCardPageFactory
from .sequence_card_image_exporter import SequenceCardImageExporter
from .sequence_card_nav_sidebar import SequenceCardNavSidebar

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceCardTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.pages: List[QWidget] = []
        self.pages_cache: dict[int, List[QWidget]] = {}
        self.initialized = False
        self.currently_displayed_length = 16
        self.nav_sidebar = SequenceCardNavSidebar(self)
        self.page_factory = SequenceCardPageFactory(self)
        self.image_exporter = SequenceCardImageExporter(self)
        self.populator = SequenceCardImagePopulator(self)
        self.cached_page_displayer = SequenceCardCachedPageDisplayer(self)
        self.image_displayer = SequenceCardImageDisplayer(self)
        self.refresher = SequenceCardRefresher(self)
        self.init_ui()

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

    def showEvent(self, event):
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.refresher.refresh_sequence_cards()
            self.initialized = True
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().showEvent(event)

    def paintEvent(self, event) -> None:
        self.background_manager = self.global_settings.setup_background_manager(self)
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
