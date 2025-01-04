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
        self._collect_all_items()
        for glyph in self.glyphs:
            glyph.setOpacity(
                1 if self.settings.glyph.should_glyph_be_visible(glyph.name) else 0.1
            )
        self.non_radial_item.setOpacity(
            1 if self.settings.grid.non_radial_visible else 0.1
        )
        self.set_clickable_items()
        self.setMouseTracking(True)
        self.add_hover_effect()
        self.setStyleSheet("border: 2px solid black;")

    def add_hover_effect(self):
        def apply_glyph_hover_effects(item: "Glyph"):
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.hoverEnterEvent = self._create_hover_enter_event(item)
            item.hoverLeaveEvent = self._create_hover_leave_event(item)
            item.setAcceptHoverEvents(True)  # Ensure hover events are accepted

            for child in item.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)
                child.setAcceptHoverEvents(True)
                child.hoverEnterEvent = self._create_hover_enter_event(item)
                child.hoverLeaveEvent = self._create_hover_leave_event(item)

        def apply_grid_hover_effects(item: "QGraphicsSvgItem"):
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.hoverEnterEvent = self._create_nonradial_hover_enter_event(item)
            item.hoverLeaveEvent = self._create_nonradial_hover_leave_event(item)
            item.setAcceptHoverEvents(True)

        for glyph in self.glyphs:
            apply_glyph_hover_effects(glyph)
        apply_grid_hover_effects(self.non_radial_item)

    def _create_hover_enter_event(self, glyph: "Glyph"):
        def hoverEnterEvent(event):
            glyph.setOpacity(0.5)

        return hoverEnterEvent

    def _create_nonradial_hover_enter_event(self, grid_item: "QGraphicsItemGroup"):
        def hoverEnterEvent(event):
            grid_item.setOpacity(0.5)

        return hoverEnterEvent

    def _create_nonradial_hover_leave_event(self, grid_item: "QGraphicsItemGroup"):
        def hoverLeaveEvent(event):
            visible = self.settings.get_grid_visibility("non_radial_points")
            if visible:
                grid_item.setOpacity(1)
            else:
                grid_item.setOpacity(0.1)

        return hoverLeaveEvent

    def _create_hover_leave_event(self, glyph: "Glyph"):
        def hoverLeaveEvent(event):
            visible = self.settings.glyph.should_glyph_be_visible(glyph.name)
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

        glyphs: list[Glyph] = [
            pictograph.tka_glyph,
            pictograph.vtg_glyph,
            pictograph.elemental_glyph,
            pictograph.start_to_end_pos_glyph,
            pictograph.reversal_glyph,
        ]
        for glyph in glyphs:
            glyph.setVisible(True)
        pictograph.grid.toggle_non_radial_points_visibility(True)

        return pictograph

    def _collect_all_items(self):
        """Return a list of all clickable items in the pictograph."""
        self.glyphs: list[Glyph] = [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

        self.non_radial_item: QGraphicsSvgItem = self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial", []
        )

    def set_clickable_items(self):
        """Enable glyphs to be clickable and toggle visibility."""
        for glyph in self.glyphs:
            glyph.mousePressEvent = self._create_glyph_mouse_press_event(glyph)
        self.non_radial_item.mousePressEvent = self.create_nonradial_mouse_press_event()

    def _create_glyph_mouse_press_event(self, glyph: "Glyph"):
        for child in glyph.childItems():
            child.setAcceptHoverEvents(True)

        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)
            if self.settings.glyph.should_glyph_be_visible(glyph.name):
                glyph.setOpacity(1)
            else:
                glyph.setOpacity(0.15)

        return mousePressEvent

    def create_nonradial_mouse_press_event(self):
        def mousePressEvent(event):
            self._toggle_grid_visibility()

            self.settings.set_grid_visibility(
                "non_radial_points",
                not self.settings.grid.non_radial_visible,
            )
            self.non_radial_item.setOpacity(
                1 if self.settings.grid.non_radial_visible else 0.1
            )

        return mousePressEvent

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle glyph visibility and synchronize with checkboxes."""
        manager = self.settings.glyph
        current_visibility = manager.should_glyph_be_visible(glyph.name)
        self.settings.set_glyph_visibility(glyph.name, not current_visibility)

        self.visibility_tab.checkbox_widget.update_checkboxes()

    def _toggle_grid_visibility(self):
        """Toggle grid visibility and synchronize with checkboxes."""
        current_visibility = self.settings.get_grid_visibility("non_radial_points")
        self.settings.grid.save_non_radial_visibility(not current_visibility)
        self.visibility_tab.checkbox_widget.update_checkboxes()

    def resizeEvent(self, event: QEvent):
        tab_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.checkbox_widget.width()
        )
        size = int(tab_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
