from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING
from objects.grid import GridPoint
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from ..prop_placement_manager import PropPlacementManager


class DefaultPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager
        self.location_points_cache = {}

    def set_prop_to_default_loc(self, prop: Prop) -> None:
        # Get location points
        if self.pictograph.check.has_strictly_placed_props():
            location_points = self.get_location_points(True)
        else:
            location_points = self.get_location_points(False)

        for location, location_point in location_points.items():
            if prop.loc == location.split("_")[0]:
                hand_point = location_point.coordinates
                self.place_prop_at_hand_point(prop, hand_point)
                return

    def place_prop_at_hand_point(self, prop: Prop, hand_point: QPointF) -> None:
        """
        Align the prop's center to the hand point using the 'centerPoint' defined in the SVG.
        """
        # Get the center point from the SVG by using the renderer and the centerPoint ID
        center_point_in_svg = self.get_svg_center_point(prop)
        
        # Map the SVG center point to scene coordinates
        center_point_in_scene = prop.mapToScene(center_point_in_svg)

        # Calculate the offset between the center point and the hand point
        offset = hand_point - center_point_in_scene

        # Apply the offset to the prop's current position
        new_position = prop.pos() + offset
        prop.setPos(new_position)

    def get_svg_center_point(self, prop: Prop) -> QPointF:
        """
        Retrieve the 'centerPoint' from the SVG.
        """
        # Use the QSvgRenderer to retrieve the coordinates of the 'centerPoint'
        element_bounding_box = prop.renderer.boundsOnElement("centerPoint")
        center_point_in_svg = element_bounding_box.center()

        return center_point_in_svg

    def get_location_points(self, strict: bool) -> dict[str, GridPoint]:
        """
        Returns hand location points, depending on whether the props should be strictly placed.
        """
        location_points = (
            self.pictograph.grid.grid_data.hand_points_strict
            if strict
            else self.pictograph.grid.grid_data.hand_points_normal
        )
        return location_points.points
