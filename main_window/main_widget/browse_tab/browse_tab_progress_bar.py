from typing import TYPE_CHECKING

from .dictionary_browser.rainbow_progress_bar import RainbowProgressBar

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabProgressBar(RainbowProgressBar):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.browse_tab = browse_tab

    def resizeEvent(self, event):
        self.setFixedWidth(self.browse_tab.width() // 3)
        self.setFixedHeight(self.browse_tab.height() // 6)

        font = self.percentage_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(self.browse_tab.width() // 40)
        self.percentage_label.setFont(font)
        self.loading_label.setFont(font)
        super().resizeEvent(event)
