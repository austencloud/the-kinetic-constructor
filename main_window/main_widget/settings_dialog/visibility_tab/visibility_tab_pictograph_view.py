from PyQt6.QtWidgets import QGraphicsItemGroup
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.pictograph_view import PictographView
from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import Qt, QEvent
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityTabPictographView(PictographView):
    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.settings = self.main_widget.settings_manager.visibility

        self.pictograph = self._initialize_example_pictograph()
        super().__init__(self.pictograph)
        for glyph in self._get_all_items():
            glyph.setOpacity(
                1
                if self.settings.glyph_visibility_manager.should_glyph_be_visible(
                    glyph.name
                )
                else 0.1
            )
        self.set_clickable_items()
        self.setMouseTracking(True)
        self.add_hover_effect()

    def add_hover_effect(self):
        def apply_hover_effects(item: "Glyph"):
            print(f"Applying hover effects to {item.name}")
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.hoverEnterEvent = self._create_hover_enter_event(item)
            item.hoverLeaveEvent = self._create_hover_leave_event(item)
            item.setAcceptHoverEvents(True)  # Ensure hover events are accepted

            for child in item.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)
                child.setAcceptHoverEvents(True)
                child.hoverEnterEvent = self._create_hover_enter_event(item)
                child.hoverLeaveEvent = self._create_hover_leave_event(item)

        for glyph in self._get_all_items():
            apply_hover_effects(glyph)

    def _create_hover_enter_event(self, glyph: "Glyph"):
        def hoverEnterEvent(event):
            glyph.setOpacity(0.5)

        return hoverEnterEvent

    def _create_hover_leave_event(self, glyph: "Glyph"):
        def hoverLeaveEvent(event):
            visible = self.settings.glyph_visibility_manager.should_glyph_be_visible(
                glyph.name
            )
            if visible:
                glyph.setOpacity(1)
            else:
                glyph.setOpacity(0.1)

        return hoverLeaveEvent

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
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            example_data
        )
        pictograph.red_reversal = True
        pictograph.blue_reversal = True
        pictograph.updater.update_pictograph(pictograph_dict)

        pictograph.tka_glyph.setVisible(True)
        pictograph.vtg_glyph.setVisible(True)
        pictograph.elemental_glyph.setVisible(True)
        pictograph.start_to_end_pos_glyph.setVisible(True)
        pictograph.reversal_glyph.setVisible(True)
        pictograph.grid.toggle_non_radial_points_visibility(True)

        return pictograph

    def _get_all_items(self) -> list[Glyph]:
        """Return a list of all clickable items in the pictograph."""
        all_glyphs = [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

        # Extend with non-radial grid points
        non_radial_items = self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial", []
        )
        if isinstance(non_radial_items, list):
            all_glyphs.extend(non_radial_items)
        else:
            all_glyphs.append(non_radial_items)

        return all_glyphs

    def set_clickable_items(self):
        """Enable glyphs to be clickable and toggle visibility."""
        for glyph in self._get_all_items():
            glyph.mousePressEvent = self._create_mouse_press_event(glyph)

    def _create_mouse_press_event(self, glyph: "Glyph"):
        for child in glyph.childItems():
            child.setAcceptHoverEvents(True)
        if glyph.name == "non_radial_points":

            def mousePressEvent(event):
                self.settings.set_grid_visibility(
                    "non_radial_points",
                    not self.settings.grid_visibility_manager.non_radial_visible,
                )
                glyph.setOpacity(
                    1
                    if self.settings.grid_visibility_manager.non_radial_visible
                    else 0.1
                )

            return mousePressEvent

        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)
            if self.settings.glyph_visibility_manager.should_glyph_be_visible(
                glyph.name
            ):
                glyph.setOpacity(1)
            else:
                glyph.setOpacity(0.15)

        return mousePressEvent

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle glyph visibility and synchronize with checkboxes."""
        manager = self.settings.glyph_visibility_manager
        current_visibility = manager.should_glyph_be_visible(glyph.name)
        if glyph.name == "non_radial_points":
            self.settings.set_grid_visibility(
                "non_radial_points", not current_visibility
            )
        else:
            self.settings.set_glyph_visibility(glyph.name, not current_visibility)
        self.visibility_tab.checkbox_widget.update_checkboxes()

    def resizeEvent(self, event: QEvent):
        tab_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.checkbox_widget.width()
        )
        size = int(tab_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
