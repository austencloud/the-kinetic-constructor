from functools import partial
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.checkbox_widget.visibility_checkbox_widget import (
        VisibilityCheckboxWidget,
    )


class VisibilityToggleCheckbox(QCheckBox):
    def __init__(
        self, name: str, visibility_checkbox_widget: "VisibilityCheckboxWidget"
    ):
        super().__init__(name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.visibility_checkbox_widget = visibility_checkbox_widget
        self.toggler = self.visibility_checkbox_widget.toggler
        self.name = name
        self._connect_signals()

    def _connect_signals(self):
        pictograph = self.visibility_checkbox_widget.visibility_tab.pictograph
        interaction_manager = pictograph.view.interaction_manager
        if self.name in self.visibility_checkbox_widget.glyph_names:
            self.stateChanged.connect(
                partial(self.toggler.toggle_glyph_visibility, self.name)
            )
            self.stateChanged.connect(
                partial(
                    interaction_manager.update_opacity, self.get_corresponding_item()
                )
            )

        else:
            self.stateChanged.connect(self.toggler.toggle_non_radial_points)
            self.stateChanged.connect(
                partial(
                    interaction_manager.update_opacity,
                    pictograph.get.non_radial_points(),
                )
            )

    def get_corresponding_item(self):
        return self.visibility_checkbox_widget.visibility_tab.pictograph.get.glyph(
            self.name
        )
