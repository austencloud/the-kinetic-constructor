from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dictionary_browser import DictionaryBrowser


class DictionaryBrowserResizer:
    def __init__(self, browser: "DictionaryBrowser"):
        self.browser = browser

