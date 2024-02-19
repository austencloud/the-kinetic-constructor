from typing import TYPE_CHECKING

from widgets.base_tab_widget import BaseTabWidget
from widgets.codex.codex import Codex
from widgets.library.library import Library
from widgets.sequence_builder.sequence_builder import SequenceBuilder

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget



class MainTabWidget(BaseTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.codex = Codex(main_widget)
        self.sequence_builder = SequenceBuilder(main_widget)
        self.library = Library(main_widget)
        self.tabs = [self.codex]
        self.addTab(self.sequence_builder, "Sequence Builder")
        self.addTab(self.codex, "Codex")
        self.addTab(self.library, "Library")

    def resize_main_tab_widget(self):
        self.codex.resize_codex()
        self.sequence_builder.resize_sequence_builder()
