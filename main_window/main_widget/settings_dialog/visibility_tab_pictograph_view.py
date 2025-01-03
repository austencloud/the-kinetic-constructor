from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsItemGroup,
    QCheckBox,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsRectItem,
)
from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.pictograph_view import PictographView
from base_widgets.base_pictograph.tka_glyph.base_glyph import BaseGlyph
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QPen

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.settings_dialog.visibility_tab import VisibilityTab

Glyph = Union[BaseGlyph, QGraphicsItemGroup, QGraphicsSvgItem]


class VisibilityTabPictographView(PictographView):
    def __init__(self, pictograph: "BasePictograph", visibility_tab: "VisibilityTab"):
        super().__init__(pictograph)
        self.visibility_tab = visibility_tab

        self.set_clickable_glyphs()

    def set_clickable_glyphs(self):
        """Enable glyphs to be clickable and update visibility settings."""
        glyphs: list[Glyph] = [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]
        for glyph in glyphs:
            glyph.mousePressEvent = self._create_mouse_press_event(glyph)
            glyph.setCursor(Qt.CursorShape.PointingHandCursor)
            glyph.setAcceptHoverEvents(True)
            glyph.hoverEnterEvent = self._create_hover_enter_event(glyph)
            glyph.hoverLeaveEvent = self._create_hover_leave_event(glyph)
            if isinstance(glyph, QGraphicsItemGroup):
                for child in glyph.childItems():
                    child.setCursor(Qt.CursorShape.PointingHandCursor)
                    child.setAcceptHoverEvents(True)
                    child.hoverEnterEvent = self._create_hover_enter_event(glyph)
                    child.hoverLeaveEvent = self._create_hover_leave_event(glyph)

    def _create_mouse_press_event(self, glyph):
        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)

        return mousePressEvent

    def _create_hover_enter_event(self, glyph):
        def hoverEnterEvent(event):
            self._add_hover_box(glyph)

        return hoverEnterEvent

    def _create_hover_leave_event(self, glyph):
        def hoverLeaveEvent(event):
            self._remove_hover_box(glyph)

        return hoverLeaveEvent

    def _add_hover_box(self, glyph: Glyph):
        """Add a red box around the glyph."""
        pen = QPen(QColor("red"))
        pen.setWidth(2)
        rect = glyph.boundingRect()
        self.hover_box = QGraphicsRectItem(rect)
        self.hover_box.setPen(pen)
        self.hover_box.setParentItem(glyph)
        self.hover_box.setZValue(glyph.zValue() + 1)

    def _remove_hover_box(self, glyph):
        """Remove the red box around the glyph."""
        if hasattr(self, "hover_box") and self.hover_box:
            self.scene().removeItem(self.hover_box)
            self.hover_box = None

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle visibility for a glyph and update the checkbox."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        manager = settings.glyph_visibility_manager

        current_visibility = manager.should_glyph_be_visible(glyph.name)
        settings.set_glyph_visibility(glyph.name, not current_visibility)
        self.visibility_tab.update_checkboxes()
