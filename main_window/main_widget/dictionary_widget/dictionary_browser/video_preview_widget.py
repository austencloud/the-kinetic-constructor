from typing import TYPE_CHECKING
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout
if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import DictionaryWidget

class VideoPreviewWidget(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        super().__init__(dictionary_widget)
        self.layout:QVBoxLayout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        self.layout.addWidget(self.web_view)
        self.setLayout(self.layout)

    def load_video(self, video_url: str):
        # Load the video URL into the QWebEngineView
        self.web_view.setUrl(QUrl(video_url))
