from typing import TYPE_CHECKING
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class VideoPreviewWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.browser = browser
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        self.layout.addWidget(self.web_view)
        self.setLayout(self.layout)

    def load_video(self, video_url: str):
        # Load the video URL into the QWebEngineView
        self.web_view.setUrl(QUrl(video_url))
