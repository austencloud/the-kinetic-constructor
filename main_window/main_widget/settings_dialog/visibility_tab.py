from copy import deepcopy
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
    QHBoxLayout,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from Enums.letters import Letter
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.pictograph_view import PictographView
from main_window.main_widget.settings_dialog.visibility_tab_pictograph_view import (
    VisibilityTabPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.glyph_checkboxes: dict[str, QCheckBox] = {}
        self.pictograph = self._initialize_example_pictograph()
        self._setup_ui()

    def _initialize_example_pictograph(self) -> BasePictograph:
        """Create and initialize the example pictograph."""
        example_data = {
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "blue_motion_type": "pro",
            "red_motion_type": "pro",
        }
        pictograph = BasePictograph(self.main_widget)
        pictograph_dict = self._find_pictograph_dict(
            letter_str=example_data["letter"],
            start_pos=example_data["start_pos"],
            end_pos=example_data["end_pos"],
            blue_motion_type=example_data["blue_motion_type"],
            red_motion_type=example_data["red_motion_type"],
        )
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph

    def _setup_ui(self):
        example_view = VisibilityTabPictographView(self.pictograph, self)
        checkbox_layout = self._setup_checkbox_layout()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addLayout(checkbox_layout)
        self.layout.addWidget(example_view)
        self.setLayout(self.layout)

    def _setup_checkbox_layout(self):
        self.header = QLabel("Visibility Settings")
        self.header.setFont(self._get_title_font())
        glyph_visibility_manager = (
            self.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.header)
        for glyph in glyph_types:
            checkbox = QCheckBox(glyph)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))
            checkbox.setFont(self._get_default_font())
            checkbox.stateChanged.connect(
                lambda state, g=glyph: self._toggle_glyph_visibility(g, state)
            )
            checkbox_layout.addWidget(checkbox)
            self.glyph_checkboxes[glyph] = checkbox
        self.spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        checkbox_layout.addItem(self.spacer)
        return checkbox_layout

    def _toggle_glyph_visibility(self, glyph: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.settings.set_glyph_visibility(glyph, is_checked)
        self._update_pictograph_visibility()

    def _update_pictograph_visibility(self):
        """Update the pictograph's visibility based on settings."""
        for glyph, checkbox in self.glyph_checkboxes.items():
            is_visible = checkbox.isChecked()
            self.settings.set_glyph_visibility(glyph, is_visible)

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        glyph_visibility_manager = (
            self.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        for glyph, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font

    def _find_pictograph_dict(
        self,
        letter_str: str,
        start_pos: str,
        end_pos: str,
        blue_motion_type: str,
        red_motion_type: str,
    ) -> Optional[dict]:
        target_letter = None
        for l in Letter:
            if l.value == letter_str:
                target_letter = l
                break
        if not target_letter:
            print(f"Warning: Letter '{letter_str}' not found in Letter Enum.")
            return None

        letter_dicts = self.main_widget.pictograph_dicts.get(target_letter, [])
        for pdict in letter_dicts:
            if (
                pdict.get("start_pos") == start_pos
                and pdict.get("end_pos") == end_pos
                and pdict.get("blue_attributes", {}).get("motion_type")
                == blue_motion_type
                and pdict.get("red_attributes", {}).get("motion_type")
                == red_motion_type
            ):
                return deepcopy(pdict)

        return None
