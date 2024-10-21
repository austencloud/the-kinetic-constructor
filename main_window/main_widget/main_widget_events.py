from typing import TYPE_CHECKING
from PyQt6.QtGui import QKeyEvent, QPainter, QCloseEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetEvents:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.main_widget.special_placement_loader.refresh_placements()
        else:
            super(self.main_widget.__class__, self.main_widget).keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self.main_widget)
        self.main_widget.background_manager.paint_background(self.main_widget, painter)

    def showEvent(self, event):
        super(self.main_widget.__class__, self.main_widget).showEvent(event)
        self.main_widget.background_handler.apply_background()
        self.main_widget.background_handler.setup_background_manager()
        self.main_widget.background_manager.start_animation()

    def hideEvent(self, event):
        super(self.main_widget.__class__, self.main_widget).hideEvent(event)
        if self.main_widget.background_manager:
            self.main_widget.background_manager.stop_animation()

    def resizeEvent(self, event) -> None:
        super(self.main_widget.__class__, self.main_widget).resizeEvent(event)
        self.main_widget.setStyleSheet(
            self.main_widget.tab_bar_styler.get_tab_stylesheet()
        )
        self.main_widget.navigation_widget.resize_navigation_widget()
        self.main_widget.menu_bar_widget.resize_menu_bar_widget()

        # Trigger resizing of components based on the current tab
        if self.main_widget.current_tab == "build":
            self.main_widget.manual_builder.resize_manual_builder()
        elif self.main_widget.current_tab == "generate":
            self.main_widget.sequence_generator.resize_sequence_generator()
        elif self.main_widget.current_tab == "dictionary":
            self.main_widget.dictionary_widget.resize_dictionary_widget()
        elif self.main_widget.current_tab == "learn":
            self.main_widget.learn_widget.resize_learn_widget()

        self.main_widget.content_layout.setStretch(0, 1)  # sequence_widget
        self.main_widget.content_layout.setStretch(1, 1)  # stacked_widget

    def closeEvent(self, event: QCloseEvent):
        self.main_widget.state_handler.save_state()
        event.accept()
