from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetBackground:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def setup_background_manager(self):
        self.main_widget.background_manager = (
            self.main_widget.settings_manager.global_settings.setup_background_manager(
                self.main_widget
            )
        )

    def apply_background(self):
        self.main_widget.background_manager = (
            self.main_widget.settings_manager.global_settings.setup_background_manager(
                self.main_widget
            )
        )
        self.main_widget.background_manager.update_required.connect(
            self.main_widget.update
        )
        self.main_widget.background_manager.start_animation()
